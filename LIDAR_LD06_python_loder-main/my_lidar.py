import serial
import struct  # To handle multi-byte values
import math

# Initialize serial connection
ser = serial.Serial(
    port='/dev/serial0',
    baudrate=230400,
    timeout=5.0,
    bytesize=8,
    parity='N',
    stopbits=1
)

running = True

while running:
    # Read the starting character (1 byte)
    data = ser.read(1)
    if data == b'\x54':  # Starting byte (0x54)
        print("New cycle detected")

        # Read the data length (1 byte)
        data_length = ser.read(1)
        data_length = struct.unpack('<B', data_length)[0]  # Convert byte to int
        print(f"Data Length: {data_length}")

        # Read radar speed (2 bytes)
        radar_speed_bytes = ser.read(2)
        radar_speed = struct.unpack('<H', radar_speed_bytes)[0]  # Little-endian 2 bytes
        print(f"Radar Speed: {radar_speed / 100.0} deg/s")  # Protocol says 0.01 deg/s

        # Read start angle (2 bytes)
        start_angle_bytes = ser.read(2)
        start_angle = struct.unpack('<H', start_angle_bytes)[0]  # Little-endian 2 bytes
        start_angle = start_angle * 0.01  # Convert to degrees
        print(f"Start Angle: {start_angle}°")

        # Read measurement data (each point is 3 bytes)
        points = []
        for _ in range(data_length):
            point_bytes = ser.read(3)
            distance, intensity = struct.unpack('<HB', point_bytes)  # 2 bytes for distance, 1 byte for intensity
            points.append((distance, intensity))
        print(f"Points: {points}")

        # Read end angle (2 bytes)
        end_angle_bytes = ser.read(2)
        end_angle = struct.unpack('<H', end_angle_bytes)[0]  # Little-endian 2 bytes
        end_angle = end_angle * 0.01  # Convert to degrees
        print(f"End Angle: {end_angle}°")

        # Read timestamp (2 bytes)
        timestamp_bytes = ser.read(2)
        timestamp = struct.unpack('<H', timestamp_bytes)[0]  # Little-endian 2 bytes
        print(f"Timestamp: {timestamp} ms")

        # Read checksum (2 bytes)
        checksum_bytes = ser.read(2)
        checksum = struct.unpack('<H', checksum_bytes)[0]  # Little-endian 2 bytes
        print(f"Checksum: {checksum}")

        # Verify checksum (optional, depends on LiDAR protocol documentation)
        # checksum_verification = ...
        # if checksum_verification != checksum:
        #     print("Checksum mismatch!")
        #     continue

        print("-" * 40)  # Separator for each cycle
