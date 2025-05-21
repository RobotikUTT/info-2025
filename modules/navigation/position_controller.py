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

    def __init__(self):
        super().__init__()
        self.config = Config().get()
        self.log = Log("PositionController")
        self.lock = Lock()

        self.running = True
        self.moving = False

        self.positionTracker = PositionTracker()
        self.speedCommunication = SpeedCommunication()

        self.target_speed = self.config["speed"]
        self.target_rotation_speed = self.config["rotation_speed"]
        self.target_acceleration = self.config["acceleration"]
        self.target_rotation_acceleration = self.config["rotation_acceleration"]
        self.update_period = 1 / self.config["update_rate"]
        self.error_pos = self.config["error_pos"]
        self.error_angle = self.config["error_angle"]

        # Position cible initiale = position actuelle
        position = self.positionTracker.getCurrentPosition()
        self.goTo(*position.get())

        self.setup()
        self.start()
        self.log.info("Contrôleur de position initialisé.")

    def setup(self):
        """Méthode d'initialisation optionnelle à redéfinir."""
        pass

    def goTo(self, x, y, w, arrivedCallback=None):
        with self.lock:
            self.target_position = Position(x, y, w)
            self.arrivedCallback = arrivedCallback
            self.moving = True
        self.log.info(f"Nouvelle position cible : x={x}, y={y}, w={w}")

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

    def run(self):
        self.log.info("Démarrage du thread de contrôle de position.")
        while self.running:
            pre_time = time.time()

            if self.moving:
                try:
                    with self.lock:
                        if self.isArrived():
                            self.moving = False
                            callback = self.arrivedCallback
                            self.log.info("Position cible atteinte.")
                            if callback and callable(callback):
                                callback()
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

    def loop(self):
        current_pos = self.positionTracker.getCurrentPosition()

        delta_pos = current_pos.delta(self.target_position)
        vect_speed = delta_pos.normalize()

        vect_speed.scalePos(self.target_speed)
        vect_speed.scaleAngle(self.target_rotation_speed)

        self.speedCommunication.sendSpeedCart(*vect_speed.get())









"""
    Base Position relative -> pas besoin de d'exécution de thread
    Version zigzag
"""
class PositionControllerZigZag():
    def __init__(self):
        self.config = Config().get()
        self.log = Log("PositionController")
        self.positionTracker = PositionTracker()
        self.speedCommunication = SpeedCommunication()

    def goTo(self, target_x, target_y, target_w):
        current_x, current_y, current_w = self.positionTracker.getCurrentPosition()
        self.speedCommunication.sendSpeedCart(target_x - current_x,
                                              target_y - current_y,
                                              target_w - current_w)

"""
    Base Vitesse
    Version PID
"""
class PositionControllerPID(PositionController):
    def setup(self):
        super().__init__()

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

            self.speedCommunication.sendSpeedCart(self.current_speed_x, self.current_speed_y, self.current_speed_w)
        except Exception as e:
            self.log.error(f"Error in run loop", e)


    def normalize(self, vect):
        x, y = vect
        d = math.sqrt(x ** 2 + y ** 2)
        if d == 0:
            return 0, 0
        return x / d, y / d