import sys
import time


class PositionTracker:
    _instance = None

    def __new__(cls):
        # Check if an instance already exists
        if cls._instance is None:
            # If not, create it
            cls._instance = super(PositionTracker, cls).__new__(cls)
        # Return the existing or newly created instance
        return cls._instance

    def __init__(self):
        # Ensure the initialization is done only once
        if not hasattr(self, 'initialized'):
            self.position = (0, 0, 0)  # Initialize position
            self.initialized = True

    def getCurrentPosition(self):
        return self.position

    def setCurrentPosition(self, position):
        self.position = position


def runExample():
    print("\nQwiic OTOS Example 1 - Basic Readings\n")

    # Create instance of device
    myOtos = qwiic_otos.QwiicOTOS()

    # Check if it's connected
    if not myOtos.is_connected():
        print("The device isn't connected to the system. Please check your connection", file=sys.stderr)
        return

    # Initialize the device
    myOtos.begin()

    print("Ensure the OTOS is flat and stationary during calibration!")
    for i in range(5, 0, -1):
        print(f"Calibrating in {i} seconds...")
        time.sleep(1)

    print("Calibrating IMU...")

    # Calibrate the IMU, which removes the accelerometer and gyroscope offsets
    myOtos.calibrateImu()

    # Reset the tracking algorithm
    myOtos.resetTracking()

    # Create PositionTracker instance (singleton)
    position_tracker = PositionTracker()

    # Main loop
    while True:
        # Get the latest position, which includes the x and y coordinates, plus
        # the heading angle
        myPosition = myOtos.getPosition()

        # Update position in the PositionTracker singleton
        position_tracker.setCurrentPosition((myPosition.x, myPosition.y, myPosition.h))

        # Print measurement
        print()
        print("Position:")
        print(f"X (Inches): {myPosition.x}")
        print(f"Y (Inches): {myPosition.y}")
        print(f"Heading (Degrees): {myPosition.h}")

        # Wait a bit to prevent spamming the serial port
        time.sleep(0.5)

        # Optionally, you can print continuously using the following code:
        # print(f"{myPosition.x}\t{myPosition.y}\t{myPosition.h}")
        # time.sleep(0.01)


if __name__ == '__main__':
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example")
        sys.exit(0)
