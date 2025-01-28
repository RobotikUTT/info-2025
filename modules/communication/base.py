import logging

from smbus2 import SMBus

from utils.config import I2cConnectionSettings


class I2CCommunication:
    def __init__(self, config: I2cConnectionSettings):
        self.log = logging.getLogger("i2c")
        self.bus = SMBus(config.bus)  # I2C bus number
        self.address = config.address  # I2C address of the device

    def write(self, data: str | list[int] | int):
        """
        Writes data to the I2C device. Can handle strings, lists of ints, or single ints.
        """
        if isinstance(data, str):
            byte_data = [ord(c) for c in data]  # Convert string to list of ASCII values
            byte_data.insert(0, 0)  # Optional: Dummy command register
            self.bus.write_i2c_block_data(self.address, byte_data[0], byte_data[1:])
            self.log.debug(f"WRITE STRING: {data}")
        elif isinstance(data, list):
            self.bus.write_i2c_block_data(self.address, data[0], data[1:])
            self.log.debug(f"WRITE LIST: {data}")
        else:
            self.bus.write_byte(self.address, data)
            self.log.debug(f"WRITE BYTE: {data}")

        self.log.info(
            f"WRITE : Data written to device at address {self.address}: {data}"
        )

    def read(self, num_bytes: int):
        """
        Reads data from the I2C device and returns it as a string.
        """
        raw_data = self.bus.read_i2c_block_data(self.address, 0, num_bytes)
        self.log.info(
            f"READ : Raw data from device at address {self.address}: {raw_data}"
        )

        # Convert received bytes to string, ignoring null bytes
        return "".join([chr(b) for b in raw_data if b != 0])
