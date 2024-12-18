from modules.communication.speed_communication import SpeedCommunication
import time
from modules.communication.i2c_communication import I2CCommunication
def main():
    i2c_comm = I2CCommunication("esp_steppers")
    while True:
        i2c_comm.write("Hello world!")
        time.sleep(0.1)
        # SpeedCommunication.sendSpeedPolar(0.2, 0.2, 0.0)





if __name__ == "__main__":
    main()
