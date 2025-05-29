from modules.communication.i2c_communication import I2CCommunication
# TODO : refactor car trouve un bus à toutes les adresses

def main():
    I2CCommunication.scan_i2c_bus()


if __name__ == "__main__":
    main()
