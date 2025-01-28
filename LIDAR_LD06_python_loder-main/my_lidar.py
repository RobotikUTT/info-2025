import serial
import struct  # To handle multi-byte values
import sys

# Check for verbosity flag
verbose = '-v' in sys.argv or '--verbose' in sys.argv

# Verbose print function
def vprint(message):
    if verbose:
        print(message)

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
        vprint("New cycle detected")

        data_length = ser.read(1)
        data_length = struct.unpack('<B', data_length)[0]  # Convert byte to int
        vprint(f"Data Length: {data_length}")

        radar_speed_bytes = ser.read(2)
        radar_speed = struct.unpack('<H', radar_speed_bytes)[0]  # Little-endian 2 bytes
        vprint(f"Radar Speed: {radar_speed / 100.0} deg/s")  # Protocol says 0.01 deg/s

        start_angle_bytes = ser.read(2)
        start_angle = struct.unpack('<H', start_angle_bytes)[0]  # Little-endian 2 bytes
        start_angle = start_angle * 0.01  # Convert to degrees
        vprint(f"Start Angle: {start_angle}°")

        points = []
        clothest = 100000000
        for _ in range(data_length):
            point_bytes = ser.read(3)
            distance, intensity = struct.unpack('<HB', point_bytes)  # 2 bytes for distance, 1 byte for intensity
            if distance < clothest:
                clothest = distance
            points.append((distance, intensity))
        vprint(f"Points: {points}")

        print(f"Clothest point : {clothest}")

        end_angle_bytes = ser.read(2)
        end_angle = struct.unpack('<H', end_angle_bytes)[0]  # Little-endian 2 bytes
        end_angle = end_angle * 0.01  # Convert to degrees
        vprint(f"End Angle: {end_angle}°")

        timestamp_bytes = ser.read(2)
        timestamp = struct.unpack('<H', timestamp_bytes)[0]  # Little-endian 2 bytes
        vprint(f"Timestamp: {timestamp} ms")

        checksum_bytes = ser.read(2)
        checksum = struct.unpack('<H', checksum_bytes)[0]  # Little-endian 2 bytes
        vprint(f"Checksum: {checksum}")

        vprint("-" * 40)  # Separator for each cycle
