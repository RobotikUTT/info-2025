from modules.communication.speed_communication import SpeedCommunication
import time
from modules.communication.i2c_communication import I2CCommunication
from math import cos, sin, pi

def main():
    speed_comm = SpeedCommunication()
    rotation_speed = 0.03
    angle = 0
    radius = 10
    while True:
        angle = (angle + rotation_speed) % (2 * pi)
        p_x = cos(angle) * radius
        p_y = sin(angle) * radius
        v_x = -p_y * rotation_speed
        v_y = p_x * rotation_speed
        time.sleep(0.1)
        speed_comm.sendSpeedCart(v_x, v_y, 0.0)



if __name__ == "__main__":
    main()
