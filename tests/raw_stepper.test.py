from modules.communication.speed_communication import SpeedCommunication
from time import sleep

def main():
    s_com = SpeedCommunication()
    s_com.sendSpeedCart(50.0, 50.0, 0);
    sleep(3)
    s_com.sendSpeedCart(0, 0, 0);

if __name__ == "__main__":
    main()