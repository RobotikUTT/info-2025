from i2c_communication import I2CCommunication
from utils.log import Log

class SpeedCommunication:
    def __init__(self):
        self.steppers_communication = I2CCommunication("esp_steppers")
        self.log = Log("I2CCommunication")

    def sendSpeedPolar(self, r, angle, rot):
        sendString = f"R: {r:.6f}, w: {angle:.6f}, r: {rot:.6f}"
        self.steppers_communication.write(sendString)

    def sendSpeedCart(self, x, y, rot):
        sendString = f"x: {x:.3f}, y: {y:.3f}, r: {rot:.3f}"
        self.steppers_communication.write(sendString)
