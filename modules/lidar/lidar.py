import time
from threading import Thread, Lock
from serial import Serial
from math import cos, sin, pi
from typing import Tuple
from utils.config import Config
from utils.log import Log

from modules.lidar.lidar_parser import parse_data


class PointData:
    # struct Teddy pr chaque point mais actuellement position robot pas utilisé
    def __init__(self, angle, distance, robot_position: Tuple[int, int], robot_angle, measured_at=0):
        self.config = Config().get()
        self.bypass_detection = self.config["detection"]["bypass_detection"]
        self.log = Log("PointData")
        self.angle = angle
        self.distance = distance
        self.robot_position = robot_position
        self.robot_angle = robot_angle
        self.x = cos(robot_angle + angle) * distance + robot_position[0]
        self.y = sin(robot_angle + angle) * distance + robot_position[1]
        self.absolute_angle = (robot_angle + angle) % (2 * pi)
        self.measured_at = measured_at

    def __str__(self):
        return f'd: {self.distance}, a: {self.angle}, x: {self.x}, y: {self.y}'

class LidarService(Thread):
    def __init__(self, position_service=None):
        super().__init__()
        self.config = Config().get()
        self.log = Log("LidarService")
        try:
            self.serial = Serial(self.config["serial"]["serial_port"], baudrate=self.config["serial"]["baudrate"], timeout=None, bytesize=8, parity="N", stopbits=1)
        except Exception as e:
            self.log.error(f'Cannot connect to I2C {self.config["serial"]["serial_port"]}: {e}')
            if not self.config["detection"]["bypass_detection"]:
                exit(1)
        self.position_service = position_service
        self.values = []
        self.observers = []

    def run(self):
        """
        Boucle principale de lecture du LIDAR et de notification des observateurs.

        Cette méthode :
            - Réinitialise le buffer d'entrée série.
            - Lit 250 octets de données depuis le LIDAR via le port série.
            - Parse les données reçues en couples (distance, angle).
            - Stocke les données dans `self.values` sous forme d'objets `PointData`.
            - Notifie tous les objets abonnés (observateurs) via le pattern Observer/Observable.

        Returns:
            None

        Notes:
            - Les données sont lues en continu (boucle infinie).
            - Si les données reçues sont invalides ou absentes, un message d'erreur est loggé.
            - Le timestamp est ajouté à chaque point pour un suivi temporel.
            - Les observateurs typiques incluent un service de détection d'obstacle (`DetectionService`)
              et un service d'affichage (`Printer`).
        """
        self.log.debug("Lidar ... ready to operate")
        while True:
            if not self.config["detection"]["bypass_detection"]:
                # self.log.debug("Lidar ... looking for real data")
                self.serial.reset_input_buffer()
                data = self.serial.read(250)

                # self.log.debug(f"Raw data length: {len(data)} - data preview: {data[:20]}") # TODO : continuer patching ici

                parsed_data = parse_data(data)
                # self.log.debug(f"{parsed_data=}")
                if not parsed_data:
                    self.log.error("No data received from LIDAR to I2C")

                self.values.clear()
                current_time = time.time()
                for distance, angle in parsed_data:
                    self.values.append(PointData(angle, distance, (0, 0), 0, current_time))

                # Programmation Observer Observable desing pattern
                # Abonnement d'objets au lIDAR pour avoir infos
                # 2 services abonnés : DetectionService et Printer
                for observer in self.observers:
                    observer.update(self.values)
            else:
                # self.log.debug("Lidar ... pass")
                pass


class DetectionService:
    # Logique de détection obstacle sur le périmètre
    def __init__(self):
        self.config = Config().get()
        self.log = Log("DetectionService")
        self.threshold = self.config["detection"]["stop_threshold"] # distance en mm pour l'arrêt
        self.stop = False
        self.stop_time = 0
        self.lock = Lock()
        self.log.info("DetectionService started")


    def update(self, points: list[float]):
        """
        Met à jour l'état d'arrêt du robot en fonction des distances mesurées.

        Args:
            points (list): Liste d'objets contenant un attribut `distance` (float),
                           représentant la distance mesurée à un obstacle.

        Returns:
            None

        Comportement:
            - Compte le nombre de points dont la distance est inférieure à un seuil (`self.threshold`)
              et différente de 0 (valeurs valides).
            - Si plus de 20 points détectent un obstacle à distance courte, le robot est stoppé.
            - Le robot reste à l'arrêt pendant au moins 1 seconde après la détection,
              puis reprend automatiquement si les conditions sont redevenues normales.
        """
        with self.lock:
            treat_dist = sum(1 for point in points if point.distance < self.threshold and point.distance != 0)
            # self.log.debug(f"Parsed data sample (first 5 points): {points[:5]}")
            if self.stop and time.time() - self.stop_time > 1:
                self.stop = False
            if treat_dist > 20:
                self.stop_time = time.time()
                self.stop = True
                self.log.info("### STOP : Obstacle detected ###")
            
class PrinterService:
    # Visualisation des données du LIDAR que pour le debug car ralentit la rasp
    def update(self, points):
        for point in points:
            print(point)
