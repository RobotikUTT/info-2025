from modules.communication.i2c_communication import I2CCommunication
from utils.log import Log

class EffectorsControl(I2CCommunication):
    def __init__(self, detect_ser):
        super().__init__("esp_effectors")
        self.log = Log("EffectorsControl")
        self.detect_ser = detect_ser

    def magnetize(self, number):
        self.write(f"1 {number}")

    def demagnetize(self, number):
        self.write(f"0 {number}")
