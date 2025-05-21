from modules.communication.i2c_communication import I2CCommunication


def main():
    I2CCommunication.scan_i2c_bus()


if __name__ == "__main__":
    main()
