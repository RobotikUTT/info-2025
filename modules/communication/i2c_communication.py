from smbus2 import SMBus
from typing import  Union
from utils.config import Config
from utils.log import Log


# test
class I2CCommunication:
    def __init__(self, device_name: str):
        self.config = Config().get()
        print(f"This is the config {self.config}")
        self.log = Log("I2CCommunication")
        self.bus = SMBus(
            self.config["i2c_mapping"][device_name]["bus"]
        )  # I2C bus number
        self.address = self.config["i2c_mapping"][device_name][
            "address"
        ]  # I2C address of the device
        print(f"This is the bus: {self.bus}, this is the address: {self.address}")

    def write(self, data: Union[str, list[int], int]):
        """
        Writes data to the I2C device. Can handle strings, lists of ints, or single ints.
        """
        try:
            if isinstance(data, str):
                # Convert string to list of ASCII values
                byte_data = [ord(c) for c in data]
                # Optional: specify the register address to write to
                register = 0x00  # Default register, change if needed
                self.bus.write_i2c_block_data(self.address, register, byte_data)
                self.log.debug(f"WRITE STRING: {data}")
            elif isinstance(data, list):
                # For list of integers, treat the first element as register
                register = data[0]  # First element is the register address
                self.bus.write_i2c_block_data(self.address, register, data[1:])
                self.log.debug(f"WRITE LIST: {data}")
            else:
                # For single integer, directly write to the device
                self.bus.write_byte(self.address, data)
                self.log.debug(f"WRITE BYTE: {data}")

            self.log.info(
            f"WRITE: Data written to device at address {self.address}: {data}"
        )
        except Exception as e:
            self.log.error(f"Error writing to I2C device: {e}")

    def read(self, num_bytes: int) -> str:
        """
        Reads data from the I2C device and returns it as a string.
        """
        try:
            # Reading the block of data from the device
            raw_data = self.bus.read_i2c_block_data(self.address, 0, num_bytes)
            self.log.info(
            f"READ: Raw data from device at address {self.address}: {raw_data}"
        )

            # Convert received bytes to string, ignore null bytes (0x00)
            return "".join([chr(b) for b in raw_data if b != 0])

        except Exception as e:
            self.log.error(f"Error reading from I2C device: {e}")
            return ""