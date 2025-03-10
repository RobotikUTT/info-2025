import time
from threading import Thread
from serial import Serial
from math import radians, cos, sin, pi
from typing import Tuple, List

PACKET_SIZE = 47

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
        self.values : List[PointData | None] = [None for _ in range(12)]
        self.observers = []

    def run(self):
        print("Lidar ... ready to operate")
        while True:
            data = self.serial.read(250)
            self.serial.reset_input_buffer()
            it = iter(data)
            try:
                while True:
                    currentData = next(it)
                    if currentData != 0x54 or next(it) != 0x2c:
                        continue
                    dataList = [0x54, 0x2c]
                    for i in range(PACKET_SIZE - 2):
                        dataList.append(next(it))
                    robot_position = (0, 0)
                    robot_angle = 0
                    now = time.time()
                    formatted = self.sortData(dataList)
                    for i, distance, angle, confidence in zip(range(12), *formatted):
                        self.values[i] = (PointData(radians(-angle % 360), distance, robot_position, robot_angle, now))
                        print(self.values[i])
                    for observer in self.observers:
                        observer.update(self.values.copy())

            except StopIteration:
                pass

    def sortData(self, dataList):
        speed = (dataList[3] << 8 | dataList[2]) / 100
        startAngle = float(dataList[5] << 8 | dataList[4]) / 100
        lastAngle = float(dataList[-4] << 8 | dataList[-5]) / 100
        if (lastAngle > startAngle):
            step = float(lastAngle - startAngle) / 11
        else:
            step = float(lastAngle + 360 - startAngle) / 11

        angle_list = []
        distance_list = []
        confidence_list = []

        for i in range(0, 12):
            distance_list.append(dataList[6 + (i * 3) + 1] << 8 | dataList[6 + (i * 3)] )
            confidence_list.append(dataList[6 + (i * 3) + 2])
            angle_list.append(step * i + startAngle)
        return distance_list, angle_list, confidence_list

class DetectionService:
    def __init__(self, threshold):
        self.threshold = threshold
        self.stop = False
        self.stop_time = 0
    def update(self, points):
        treat_dist = sum(1 for point in points if point.distance < self.threshold)

        if self.stop and time.time() - self.stop_time > 3:
            self.stop = False  # Resume movement after 4 seconds
        elif not self.stop and treat_dist > 1:
            self.stop_time = time.time()
            self.stop = True  # Stop if more than 1 point is too close
