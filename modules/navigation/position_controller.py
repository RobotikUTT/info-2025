from abc import ABC, abstractmethod
from simple_pid import PID
from modules.slam.position_tracker import PositionTracker
from threading import Thread, Lock
from utils.config import Config
from utils.log import Log
import math
from modules.communication.speed_communication import SpeedCommunication
import time
from utils.position import Position



class PositionController(Thread, ABC):
    """
    Classe abstraite pour le contrôle de la position.
    Hérite de Thread.
    Force à implémenter loop en fonction du type de controller.
    """

    def __init__(self, lidar_service, detection_service):
        super().__init__()
        self.config = Config().get()
        self.log = Log("PositionController")
        self.lock = Lock()

        self.running = True
        self.moving = False

        self.positionTracker = PositionTracker()
        self.speedCommunication = SpeedCommunication()
        self.detection_service = detection_service
        lidar_service.observers += [detection_service]

        self.target_speed = self.config["PositionController"]["speed"]
        self.target_rotation_speed = self.config["PositionController"]["rotation_speed"]
        self.target_acceleration = self.config["PositionController"]["acceleration"]
        self.target_rotation_acceleration = self.config["PositionController"]["rotation_acceleration"]
        self.update_period = 1 / self.config["PositionController"]["update_rate"]
        self.error_pos = self.config["PositionController"]["error_pos"]
        self.error_angle = self.config["PositionController"]["error_angle"]

        # Position cible initiale = position actuelle
        position = self.positionTracker.getCurrentPosition()
        self.goTo(*position.get())

        self._setup()
        self.log.info("Contrôleur de position initialisé.")

    @abstractmethod
    def _setup(self): # Méthode inutile si pas instancié -> TODO refactor le init dans un _setup
        """Méthode d'initialisation optionnelle à redéfinir."""
        pass

    def goToRelative(self, x, y, w, arrivedCallback=None):
        current_pos = self.positionTracker.getCurrentPosition()
        destination = current_pos.add(Position(x, y, w))
        self.goTo(*destination.get(), arrivedCallback)


    def goTo(self, x, y, w, arrivedCallback=None):
        self.log.info(f"Nouvelle position cible : x={x}, y={y}, w={w}")
        self.target_position = Position(x, y, w)
        self.arrivedCallback = arrivedCallback
        self.moving = True

    def isArrived(self):
        current_pos = self.positionTracker.getCurrentPosition()
        return current_pos.equal(self.target_position, self.error_pos, self.error_angle)

    def stop(self):
        """Arrête proprement le thread."""
        self.running = False
        self.join()
        self.log.info("Contrôleur de position arrêté.")

    @abstractmethod
    def loop(self):
        pass

    @abstractmethod
    def obstacleDetected(self):
        pass

    def run(self):
        self.log.info("Démarrage du thread de contrôle de position.")
        while self.running:
            pre_time = time.time()
            if self.moving:
                # self.log.debug(f"Detection {self.detection_service.stop}")
                try:
                    with self.lock:
                        if self.isArrived():
                            self.moving = False
                            self.speedCommunication.sendSpeedCart(0, 0, 0)
                            callback = self.arrivedCallback
                            self.log.info("Position cible atteinte.")
                            if callback and callable(callback):  # WTF is this ? Type confusion
                                callback()
                        if self.detection_service.stop:
                            self.speedCommunication.sendSpeedCart(0, 0, 0)
                            self.obstacleDetected()
                        else:
                            self.loop()
                except Exception as e:
                    self.log.error(f"Erreur dans la boucle de contrôle", e)

            delta_time = time.time() - pre_time
            sleep_time = self.update_period - delta_time
            if sleep_time > 0:
                time.sleep(sleep_time)
            else:
                self.log.warn(f"Boucle trop lente ({delta_time:.4f}s), périodicité non respectée.")


class PositionControllerLinear(PositionController):
    """
    Contrôleur de position basé sur une correction linéaire simple.
    """

    def __init__(self, lidar_service, detection_service):
        super().__init__(lidar_service, detection_service)
        self.log = Log("PositionControllerLinear")

    def loop(self):
        current_pos = self.positionTracker.getCurrentPosition()
        # self.log.debug(f"Current position : {current_pos}")

        delta_pos = self.target_position.minus(current_pos)
        vect_speed = delta_pos.normalize().rotate(-current_pos.w)

        current_vel = self.positionTracker.getCurrentVelocity()
        current_speed = current_vel.norm()
        # self.log.debug(f"Current vel : {current_vel}")
        # self.log.debug(f"Current speed : {current_speed}")
        position_error = delta_pos.norm()
        # self.log.debug(f"current real speed : {current_speed}")
        speed = max(min(current_speed + self.target_acceleration, position_error, self.target_speed), 0.005)
        vect_speed.multiplyPos(speed * 2.4)

        angle_error = delta_pos.w
        # angle_error = self.target_position.w - current_pos
        angle_coeff = min(abs(angle_error), self.target_rotation_speed)
        vect_speed.multiplyAngle(-angle_coeff)
        vec_cpy = vect_speed.rotate(2.512)
        # self.log.debug(f"Valeurs : {vec_cpy.x}, {vec_cpy.y}, {vec_cpy.w}")
        self.speedCommunication.sendSpeedCart(*vec_cpy.get())

    def _setup(self):
        pass

    def obstacleDetected(self):
        pass









"""
    Base Position relative -> pas besoin de d'exécution de thread
    Version zigzag
"""
class PositionControllerZigZag(PositionController):
    def __init__(self, detection_service):
        super().__init__(detection_service)
        self.log = Log("PositionControllerZigZag")
        self.positionTracker = PositionTracker()
        self.speedCommunication = SpeedCommunication()


    def goTo(self, target_x, target_y, target_w, arrivedCallback=None):
        current_x, current_y, current_w = self.positionTracker.getCurrentPosition()
        self.speedCommunication.sendSpeedCart(target_x - current_x,
                                              target_y - current_y,
                                              target_w - current_w)

"""
    Base Vitesse
    Version PID
"""
class PositionControllerPID(PositionController):
    def __init__(self, detection_service):
        super().__init__(detection_service)
        self.log = Log("PositionControllerPID")

    def _setup(self):

        # PID Controllers
        p_pos = self.config["PID_position"]["P"]
        i_pos = self.config["PID_position"]["I"]
        d_pos = self.config["PID_position"]["D"]
        self.pid_x = PID(p_pos, i_pos, d_pos)
        self.pid_y = PID(p_pos, i_pos, d_pos)

        p_angle = self.config["PID_angle"]["P"]
        i_angle = self.config["PID_angle"]["I"]
        d_angle = self.config["PID_angle"]["D"]
        self.pid_w = PID(p_angle, i_angle, d_angle)

        x, y, w = self.positionTracker.getCurrentPosition()
        self.target_pos_x = x
        self.target_pos_y = y
        self.target_pos_w = w

        self.current_speed_x = 0
        self.current_speed_y = 0
        self.current_speed_w = 0
        self.pre_time = time.time()

    def loop(self):
        try:
            delta_time = time.time() - self.pre_time
            pre_time = time.time()

            current_pos_x, current_pos_y, current_pos_w = self.positionTracker.getCurrentPosition()

            with self.lock:
                control_x = self.pid_x(current_pos_x)
                control_y = self.pid_y(current_pos_y)
                control_w = self.pid_w(current_pos_w)

            pid_speed = math.sqrt(control_x ** 2 + control_y ** 2)

            if pid_speed > self.target_speed:
                current_speed = math.sqrt(self.current_speed_x ** 2 + self.current_speed_y ** 2)
                if current_speed < self.target_speed:
                    current_speed += self.target_acceleration * delta_time

                d_x, d_y = self.normalize((self.target_pos_x - current_pos_x, self.target_pos_y - current_pos_y))

                self.current_speed_x = current_speed * d_x
                self.current_speed_y = current_speed * d_y
            else:
                self.current_speed_x = control_x
                self.current_speed_y = control_y

            self.current_speed_w = control_w

            self.speedCommunication.sendSpeedCart(self.current_speed_x, self.current_speed_y, 0) # self.current_speed_w)
        except Exception as e:
            self.log.error(f"Error in run loop", e)


    def normalize(self, vect):
        x, y = vect
        d = math.sqrt(x ** 2 + y ** 2)
        if d == 0:
            return 0, 0
        return x / d, y / d