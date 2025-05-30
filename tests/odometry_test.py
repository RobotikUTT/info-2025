from modules.lidar.lidar import DetectionService, LidarService
from modules.communication.speed_communication import SpeedCommunication
from time import sleep, time
from math import sin

def main():
    ld = LidarService()
    ld.start()
    ds = DetectionService()
    ld.observers += [ds]
    sp = SpeedCommunication()
    speed = 0.2

    direction = 1
    begin = time()
    state = 0
    while 1:
        if ds.stop:
            sp.sendSpeedCart(0, 0, 0)

        else:
            sp.sendSpeedCart(direction*sin(state)*speed, direction*sin(state)*speed, 0)
            state += 0.1

        sleep(0.1)

def main2():
    ld = LidarService()
    ld.start()
    ds = DetectionService()
    ld.observers += [ds]
    sp = SpeedCommunication()
    def inner():
        while True:
            print("forward")
            sp.sendSpeedCart(0.5, 0.5, 0)
            begin = time()
            while time() - begin < 2:
                if ds.stop:
                    return
                sleep(0.1)

            print("backward")
            sp.sendSpeedCart(-0.5, -0.5, 0)
            begin = time()
            while time() - begin < 2:
                if ds.stop:
                    return
                sleep(0.1)
    inner()
    sp.sendSpeedCart(0, 0, 0)


if __name__ == "__main__":
    main()
