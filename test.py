import smbus2
import time

# I2C settings
I2C_SLAVE_ADDRESS = 0x08  # The I2C address of the ESP32
bus = smbus2.SMBus(1)  # Use I2C bus 1 on the Raspberry Pi

while True:
    try:
        # Send a message to the ESP32
        message = "Hello ESP32!"
        data = [ord(char) for char in message]
        bus.write_i2c_block_data(I2C_SLAVE_ADDRESS, 0x00, data)
        print(f"Sent: {message}")
        
        # Wait for 1 second
        time.sleep(1)
    except Exception as e:
        print(f"Error: {e}")
        break
