import time
from serial import Serial
from math import pi, sin, cos
from utils.config import Config
from utils.log import Log
from modules.lidar.lidar_parser import parse_data

# Initialisation config et log
config = Config().get()
log = Log("LidarCounter")
threshold = config["detection"]["stop_threshold"]

# Connexion série
try:
    serial = Serial(
        config["serial"]["serial_port"],
        baudrate=config["serial"]["baudrate"],
        timeout=None,
        bytesize=8,
        parity="N",
        stopbits=1
    )
except Exception as e:
    log.error(f"Erreur de connexion au port série : {e}")
    exit(1)

log.info("Démarrage du script de comptage des treat_points")

while True:
    serial.reset_input_buffer()
    data = serial.read(15000)

    parsed_data = parse_data(data)
    if not parsed_data:
        log.error("Aucune donnée LIDAR reçue")
        continue

    current_time = time.time()
    treat_points = 0

    for distance, angle in parsed_data:
        if distance < threshold and distance != 0:
            treat_points += 1

    print(f"Nombre de points proches (treat_points): {treat_points}")
    time.sleep(0.1)  # Petite pause pour éviter de spammer
