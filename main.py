from modules.communication.speed_communication import SpeedCommunication
import time
from math import cos, sin, pi
from modules.lidar.lidar import LidarService, DetectionService, PrinterService

def main():
    lidar_service = LidarService()
    lidar_service.start()
    detection_service = DetectionService(200)
    printer_service = PrinterService()
    lidar_service.observers += [detection_service]
    speed_comm = SpeedCommunication(detection_service)
    rotation_speed = 0.1
    angle = 0
    radius = 4
    while True:
        if not detection_service.stop:
            angle = (angle + rotation_speed) % (2 * pi)
            p_x = cos(angle) * radius
            p_y = sin(angle) * radius
            v_x = -p_y * rotation_speed
            v_y = p_x * rotation_speed
            time.sleep(0.1)
            speed_comm.sendSpeedCart(v_x, v_y, 0.0)

if __name__ == "__main__":
    main()
