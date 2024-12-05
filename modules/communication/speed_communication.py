from i2c_communication import I2CCommunication

class SpeedCommunication:
    def __init__(self):
        self.steppers_communication = I2CCommunication("esp_steppers")
        self.log = Log("I2CCommunication")

    def sendSpeedPolar(self, r, angle, rot):
        sendString = f"R: {r:.6f}, w: {angle:.6f}, r: {rot:.6f}"
        self.steppers_communication.write(sendString)

    def sendSpeedCart(self, x, y, rot):
        sendString = f"x: {x:.6f}, y: {y:.6f}, r: {rot:.6f}"
        self.steppers_communication.write(sendString)

