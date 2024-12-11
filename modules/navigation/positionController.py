from simple_pid import PID
from modules.slam.position_tracker import PositionTracker
from threading import Thread, Lock
from utils.config import Config
from utils.log import Log
import math
from modules.communication.speed_communication import SpeedCommunication
import time


class PositionController:
    def __init__(self):
        self.config = Config().get()
        self.log = Log("position_controller")

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

        # Position tracker and communication
        self.positionTracker = PositionTracker()
        self.speedCommunication = SpeedCommunication()

        x, y, w = self.positionTracker.getCurrentPosition()
        self.targetPosX = x
        self.targetPosY = y
        self.targetPosW = w

        self.target_speed = self.config["speed"]
        self.target_acceleration = self.config["acceleration"]

        self.lock = Lock()
        self.running = True

        # Start navigation loop
        self.controllerLoop = Thread(target=self.run)
        self.controllerLoop.start()

    def goTo(self, x, y, w):
        with self.lock:
            self.targetPosX = x
            self.targetPosY = y
            self.targetPosW = w
            self.pid_x.setpoint = x
            self.pid_y.setpoint = y
            self.pid_w.setpoint = w

    def run(self):
        current_speed_x = 0
        current_speed_y = 0
        current_speed_w = 0
        pre_time = time.time()

        while self.running:
            try:
                delta_time = time.time() - pre_time
                pre_time = time.time()

                current_pos_x, current_pos_y, current_pos_w = self.positionTracker.getCurrentPosition()

                with self.lock:
                    control_x = self.pid_x(current_pos_x)
                    control_y = self.pid_y(current_pos_y)
                    control_w = self.pid_w(current_pos_w)

                pid_speed = math.sqrt(control_x**2 + control_y**2)

                if pid_speed > self.target_speed:
                    current_speed = math.sqrt(current_speed_x**2 + current_speed_y**2)
                    if current_speed < self.target_speed:
                        current_speed += self.target_acceleration * delta_time

                    d_x, d_y = self.normalize((self.targetPosX - current_pos_x, self.targetPosY - current_pos_y))

                    current_speed_x = current_speed * d_x
                    current_speed_y = current_speed * d_y
                else:
                    current_speed_x = control_x
                    current_speed_y = control_y

                current_speed_w = control_w

                self.speedCommunication.sendSpeedCart(current_speed_x, current_speed_y, current_speed_w)
            except Exception as e:
                self.log.error(f"Error in run loop: {e}")

    def normalize(self, vect):
        x, y = vect
        d = math.sqrt(x**2 + y**2)
        if d == 0:
            return 0, 0
        return x / d, y / d
