from modules.communication.i2c_communication import I2CCommunication
from utils.log import Log

class SpeedCommunication(I2CCommunication):
    def __init__(self, detect_ser):
        super().__init__("esp_steppers")
        self.log = Log("I2CCommunication")
        self.detect_ser = detect_ser

    def sendSpeedPolar(self, r, angle, rot):
        if self.detect_ser.stop:
            self.write("R: 0.0, w: 0.0, r: 0.0")
        else:
            sendString = f"R: {r:.6f}, w: {angle:.6f}, r: {rot:.6f}"
            self.write(sendString)

    def sendSpeedCart(self, x, y, rot):
        if self.detect_ser.stop:
            self.write("x: 0.0, y: 0.0, r: 0.0")
        else:
            sendString = f"x: {x:.3f}, y: {y:.3f}, r: {rot:.3f}"
            self.write(sendString)
