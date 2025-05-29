from serial import Serial

class SerialReader:
    def __init__(self):
        self.serial = Serial(
            "/dev/serial0",
            baudrate=230400,
            timeout=None,
            bytesize=8,
            parity="N",
            stopbits=1
        )

    def read_loop(self):
        print("Lecture série démarrée...")
        while True:
            if self.serial.in_waiting > 0:
                data = self.serial.readline().decode('utf-8', errors='replace').strip()
                print(f"Reçu : {data}")

if __name__ == "__main__":
    reader = SerialReader()
    reader.read_loop()
