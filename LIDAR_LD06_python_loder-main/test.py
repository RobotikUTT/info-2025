import logging
import serial

logging.basicConfig(level=logging.INFO)
ser = serial.Serial(port='/dev/serial0', baudrate=230400, timeout=1)

while True:
    try:
        data = ser.read()
        if data:
            logging.info(f"Data received: {data}")
        else:
            logging.info("No data")
    except KeyboardInterrupt:
        logging.info("Program interrupted. Exiting...")
        break
