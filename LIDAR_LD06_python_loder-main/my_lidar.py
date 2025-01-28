import serial
import struct  # To handle multi-byte values
import pygame
import numpy as np

# Initialize serial connection
ser = serial.Serial(
    port='/dev/serial0',
    baudrate=230400,
    timeout=5.0,
    bytesize=8,
    parity='N',
    stopbits=1
)

# Initialize Pygame
pygame.init()
size = 600
screen = pygame.display.set_mode((size, size))
origin = (size // 2, size // 2)
scale = size // 2 / 4000  # Adjust scale for distance visualization (assuming distance in mm)

def draw(points, start_angle, stop_angle):
    screen.fill((255, 255, 255))

    # Calculate the angle step size
    angles = np.linspace(start_angle, stop_angle, len(points))

    for point, angle in zip(points, angles):
        distance, _ = point
        # Convert polar coordinates to Cartesian
        p_x = origin[0] + np.cos(np.deg2rad(angle)) * distance * scale
        p_y = origin[1] - np.sin(np.deg2rad(angle)) * distance * scale  # Invert Y-axis for screen coordinates
        pygame.draw.line(screen, (0, 0, 0), origin, (p_x, p_y))

    pygame.display.flip()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

    # Read the starting character (1 byte)
    data = ser.read(1)
    if data == b'\x54':  # Starting byte (0x54)

        # Read data length
        data_length = struct.unpack('<B', ser.read(1))[0]

        # Read radar speed (not used here)
        radar_speed = struct.unpack('<H', ser.read(2))[0]

        # Read start angle
        start_angle = struct.unpack('<H', ser.read(2))[0] * 0.01  # Convert to degrees

        # Read measurement points
        points = []
        for _ in range(data_length):
            point_bytes = ser.read(3)
            distance, intensity = struct.unpack('<HB', point_bytes)  # 2 bytes for distance, 1 byte for intensity
            points.append((distance, intensity))

        # Read end angle
        end_angle = struct.unpack('<H', ser.read(2))[0] * 0.01  # Convert to degrees

        # Draw the points
        draw(points, start_angle, end_angle)

        # Read timestamp (optional)
        timestamp = struct.unpack('<H', ser.read(2))[0]
