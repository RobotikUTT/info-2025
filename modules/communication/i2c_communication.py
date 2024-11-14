# modules/communication/i2c_communication.py
from typing import Optional

from utils.log import Log
from utils.config import Config
import smbus2


class I2CCommunication:
    def __init__(self, device_name: str):
        self.config = Config().get()
        self.log = Log("I2CCommunication")
        self.bus = smbus2.SMBus(self.config["i2c_mapping"][device_name]["bus"])  # I2C bus number, e.g., 1 for Raspberry Pi
        self.address = self.config["i2c_mapping"][device_name]["address"]  # I2C address of the device


    def write(self, data: Optional[list[int] | int]):
        """
        Writes data to the I2C device.
        """
        # data : first is starting register
        # After it is Sequence[int]
        if isinstance(data, list):
            # Writing a block of data
            self.log.debug(f"WRITE : {data}")
            self.bus.write_i2c_block_data(self.address, data[0], data[1:])
        else:
            # Writing a single byte
            self.log.debug(f"WRITE : {data}")
            self.bus.write_byte(self.address, data)
        self.log.info(f"WRITE : Data written to device at address {self.address}: {data}")

    def read(self, num_bytes: int):
        """
        Reads data from the I2C device.
        """
        data = self.bus.read_i2c_block_data(self.address, 0, num_bytes)
        self.log.info(f"READ : Data read from device at address {self.address}: {data}")
        return data

    def close(self):
        """
        Closes the I2C bus.
        """
        self.log.info("CLOSE : I2C bus closed")
        self.bus.close()
