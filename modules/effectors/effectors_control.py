from modules.communication.i2c_communication import I2CCommunication
from utils.config import Config
from utils.log import Log
from smbus2 import SMBus

"""
Contrôle des effecteurs via I2C vers l'ESP :
  ID 0 : pince (Everything)  → state 0 = putDownEverything, state 1 = takeEverything
  ID 1 : bannière            → state 0 = setBannerClose,   state 1 = setBannerOpen
"""

class EffectorsControl(I2CCommunication):
    def __init__(self, device_name: str):
        super().__init__("esp_effectors")
        self.bus = SMBus(
            self.config["i2c_mapping"][device_name]["bus"]
        )  # I2C bus number
        self.address = self.config["i2c_mapping"][device_name][
            "address"
        ]  # I2C address of the device

        # self.config = Config().get()
        self.log = Log("EffectorsControl")

    def put_down_everything(self):
        """ID 0, state 0 → putDownEverything"""
        # self.log.debugg("Envoi de la commande putDownEverything")
        self.write("0 0")

    def take_everything(self):
        """ID 0, state 1 → takeEverything"""
        # self.log.debugg("Envoi de la commande takeEverything")
        self.write("1 0")

    def set_banner_close(self):
        """ID 1, state 0 → setBannerClose"""
        # self.log.debugg("Envoi de la commande setBannerClose")
        self.write("0 1")

    def set_banner_open(self):
        """ID 1, state 1 → setBannerOpen"""
        # self.log.debugg("Envoi de la commande setBannerOpen")
        self.write("1 1")
