import json
import time
from modules.communication.speed_communication import SpeedCommunication
from pathlib import Path
from math import sqrt
from utils.config import Config
from utils.log import Log

class PathChecker(SpeedCommunication):
    # Hérite de SpeedCommunication pour l'envoi des vitesse
    def __init__(self, detect_service):
        self.config = Config().get()
        self.log = Log("PathChecker")
        path_obj = Path(self.config["run"]["path_file"])
        filename = path_obj.resolve()

        super().__init__(detect_service)
        self.path = self.load_path(filename)

        self.speeds = []
        self._generate_speeds()

    def load_path(self, filename):
        """Load the path from a JSON file."""
        try:
            with open(filename, "r") as f:
                return [(x, y) for x, y in json.load(f)]
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.log.error(f"Error loading path file: {e}")
            return []


    def _generate_speeds(self):
        """
        Génère les vecteurs de vitesses normalisés à partir du chemin défini.

        Pour chaque segment consécutif du chemin (`self.path`), cette méthode :
            - Calcule le vecteur directionnel entre deux points.
            - Normalise ce vecteur à la vitesse désirée définie dans `self.config["run"]["speed"]`.
            - Stocke le vecteur de vitesse (dx, dy) dans `self.speeds`.

        Returns:
            None

        Notes:
            - Assure que chaque segment est parcouru à vitesse constante, indépendamment de sa longueur.
            - La liste `self.speeds` contiendra un vecteur par segment du chemin.
        """
        for i in range(len(self.path) - 1):
            x1, y1 = self.path[i]
            x2, y2 = self.path[i + 1]
            dx = (x2 - x1)
            dy = (y2 - y1)
            dist = sqrt(dx**2 + dy**2)
            dx = dx * self.config["run"]["speed"]/dist
            dy = dy * self.config["run"]["speed"]/dist
            self.speeds.append((dx, dy))

    def rotate360(self):
        # Future function to only rotate
        return 0,0,0.8


    def start(self):
        """Follow the path by sending speed commands."""

        for x, y in self.speeds:
            time.sleep(self.config["run"]["instruction_delay"])
            self.sendSpeedCart(x, y, 0, 0)

            """
            Envoi vitesse, à exécuter en x temps, soit vitesse et distance en cm soit temps
            """
