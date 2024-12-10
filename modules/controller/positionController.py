from simple_pid import PID
from modules.position_tracker.position_tracker import PositionTracker
from threading import Thread
from threading import Lock
from utils.config import Config
from utils.log import Log
import math
from modules.communication.speed_communication import SpeedCommunication
import time

class positionController:
    def __int__(self):
        self.config = Config().get()
        self.log = Log("position_controller")

        p_pos = self.config["PID_position"]["P"]
        i_pos = self.config["PID_position"]["I"]
        d_pos = self.config["PID_position"]["D"]
        self.pid_x = PID(p_pos, i_pos, d_pos)
        self.pid_y = PID(p_pos, i_pos, d_pos)

        p_angle = self.config["PID_angle"]["P"]
        i_angle = self.config["PID_angle"]["I"]
        d_angle = self.config["PID_angle"]["D"]
        self.pid_w = PID(p_angle, i_angle, d_angle)

        self.positionTracker = PositionTracker()
        self.speedCommunication = SpeedCommunication()

        x, y, w = self.positionTracker.getCurrentPosition()
        self.targetPosX = x
        self.targetPosY = y
        self.targetPosW = w

        self.target_speed = self.config["speed"]
        self.target_acceleration = self.config["acceleration"]

        controllerLoop = Thread(self.run())
        self.lock = Lock()
        controllerLoop.start()

    def goTo(self, x, y, w):
        self.targetPosX = x
        self.targetPosY = y
        self.targetPosW = w
        with self.lock:
            self.pid_x.setpoint(x)
            self.pid_y.setpoint(y)
            self.pid_w.setpoint(w)

    def run(self):

        pre_time = time.time()


        while True:
            delta_time = pre_time - time.time()
            pre_time = time.time()

            current_pos_x, current_pos_y, current_pos_w = self.positionTracker.getCurrentPosition()
            with self.lock:
                control_x = self.pid_x(current_pos_x)
                control_y = self.pid_y(current_pos_y)
                control_w = self.pid_w(current_pos_w)

            pid_speed = math.sqrt(control_x**2 + control_y**2)

            if pid_speed > self.target_speed:

                current_speed = math.sqrt(current_x**2 + current_y**2)

                if not current_speed > self.target_speed:
                    # acceleration
                    current_speed = current_speed + self.target_acceleration * delta_time

                    direction_x = current_speed * (self.targetPosX - current_x)/
                    direction_y = current_speed

                    current_x = current_speed *


            else:
                pass






