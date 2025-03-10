import time
from threading import Thread
from serial import Serial
from math import cos, sin, pi
from typing import Tuple

from modules.lidar.flowpy_lidar import parse_data


class PointData:
    def __init__(self, angle, distance, robot_position: Tuple[int, int], robot_angle, measured_at=0):
        self.angle = angle
        self.distance = distance
        self.robot_position = robot_position
        self.robot_angle = robot_angle
        self.x = cos(robot_angle + angle) * distance + robot_position[0]
        self.y = sin(robot_angle + angle) * distance + robot_position[1]
        self.absolute_angle = (robot_angle + angle) % (2 * pi)
        self.measured_at = measured_at

    def __str__(self):
        return f'd: {self.distance}, a: {self.angle}, x: {self.x}, y: {self.y}'

class LidarService(Thread):
    def __init__(self, position_service=None):
        super().__init__()
        self.serial = Serial("/dev/serial0", baudrate=230400, timeout=None, bytesize=8, parity="N", stopbits=1)
        self.position_service = position_service
        self.values = []
        self.observers = []

    def run(self):
        print("Lidar ... ready to operate")
        while True:
            self.serial.reset_input_buffer()
            data = self.serial.read(250)

            parsed_data = parse_data(data)

            self.values.clear()
            current_time = time.time()
            for distance, angle in parsed_data:
                self.values.append(PointData(angle, distance, (0, 0), 0, current_time))

            for observer in self.observers:
                observer.update(self.values)


class DetectionService:
    def __init__(self, threshold):
        self.threshold = threshold
        self.stop = False
        self.stop_time = 0
    def update(self, points):
        treat_dist = sum(1 for point in points if point.distance < self.threshold and point.distance != 0)
        if self.stop and time.time() - self.stop_time > 1:
            self.stop = False
        if treat_dist > 20:
            self.stop_time = time.time()
            self.stop = True
            
class PrinterService:
    def update(self, points):
        for point in points:
            print(point)
