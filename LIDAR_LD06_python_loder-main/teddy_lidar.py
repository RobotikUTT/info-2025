import pygame
import time
from threading import Thread, Lock
from serial import Serial
from math import radians, cos, sin, pi
from typing import Tuple, List

PACKET_SIZE = 47

# ---------------------- DEFINE CYCLIC REDUNDANCY CHECK TABLE ----------------------

CRC_TABLE = b"\x00\x4d\x9a\xd7\x79\x34\xe3\xae\xf2\xbf\x68\x25\x8b\xc6\x11\x5c" \
            b"\xa9\xe4\x33\x7e\xd0\x9d\x4a\x07\x5b\x16\xc1\x8c\x22\x6f\xb8\xf5" \
            b"\x1f\x52\x85\xc8\x66\x2b\xfc\xb1\xed\xa0\x77\x3a\x94\xd9\x0e\x43" \
            b"\xb6\xfb\x2c\x61\xcf\x82\x55\x18\x44\x09\xde\x93\x3d\x70\xa7\xea" \
            b"\x3e\x73\xa4\xe9\x47\x0a\xdd\x90\xcc\x81\x56\x1b\xb5\xf8\x2f\x62" \
            b"\x97\xda\x0d\x40\xee\xa3\x74\x39\x65\x28\xff\xb2\x1c\x51\x86\xcb" \
            b"\x21\x6c\xbb\xf6\x58\x15\xc2\x8f\xd3\x9e\x49\x04\xaa\xe7\x30\x7d" \
            b"\x88\xc5\x12\x5f\xf1\xbc\x6b\x26\x7a\x37\xe0\xad\x03\x4e\x99\xd4" \
            b"\x7c\x31\xe6\xab\x05\x48\x9f\xd2\x8e\xc3\x14\x59\xf7\xba\x6d\x20" \
            b"\xd5\x98\x4f\x02\xac\xe1\x36\x7b\x27\x6a\xbd\xf0\x5e\x13\xc4\x89" \
            b"\x63\x2e\xf9\xb4\x1a\x57\x80\xcd\x91\xdc\x0b\x46\xe8\xa5\x72\x3f" \
            b"\xca\x87\x50\x1d\xb3\xfe\x29\x64\x38\x75\xa2\xef\x41\x0c\xdb\x96" \
            b"\x42\x0f\xd8\x95\x3b\x76\xa1\xec\xb0\xfd\x2a\x67\xc9\x84\x53\x1e" \
            b"\xeb\xa6\x71\x3c\x92\xdf\x08\x45\x19\x54\x83\xce\x60\x2d\xfa\xb7" \
            b"\x5d\x10\xc7\x8a\x24\x69\xbe\xf3\xaf\xe2\x35\x78\xd6\x9b\x4c\x01" \
            b"\xf4\xb9\x6e\x23\x8d\xc0\x17\x5a\x06\x4b\x9c\xd1\x7f\x32\xe5\xa8"

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
        self.values: List[PointData] = []
        self.lock = Lock()

    def run(self):
        dataList = []
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
                    with self.lock:  # Lock access to the shared values list
                        self.values.clear()
                        for distance, angle, confidence in zip(*formatted):
                            self.values.append(PointData(radians(-angle % 360), distance, robot_position, robot_angle, now))
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

    def getValues(self):
        with self.lock:  # Lock access to the shared values list
            return self.values

if __name__ == "__main__":
    ld = LidarService()
    ld.start()
    # Initialize Pygame
    pygame.init()
    size = 600
    screen = pygame.display.set_mode((size, size))
    origin = (size // 2, size // 2)
    scale = 2  # Adjust scale for distance visualization (assuming distance in mm)
    clock = pygame.time.Clock()

    def draw():
        screen.fill((255, 255, 255))

        values = ld.getValues()
        for value in values:
            print(value)
            pygame.draw.line(screen, (0, 0, 0), origin, (value.x, value.y))

        pygame.display.flip()

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
        draw()
        clock.tick(10)

    pygame.quit()
