from modules.communication.speed_communication import SpeedCommunication
import time
from modules.communication.i2c_communication import I2CCommunication
import math

def main():
    speed_comm = SpeedCommunication()
    x = 0
    while True:
        x += 1
        time.sleep(0.1)
        speed_comm.sendSpeedCart(math.cos(x)*0.2, 0.0, 0.0)



if __name__ == "__main__":
    main()
