import json
import time
from modules.communication.speed_communication import SpeedCommunication
from pathlib import Path
from math import sqrt
from utils.config import Config
from utils.log import Log

class PathFollower(SpeedCommunication):
    # Hérite de SpeedCommunication pour l'envoi des vitesse
    def __init__(self, detect_service):
        self.config = Config().get()
        self.log = Log("PathFollower")
        path_obj = Path(self.config["run"]["path_file"])
        filename = path_obj.resolve()

        super().__init__(detect_service)
        self.path = self.load_path(filename)

        self.speeds = []
        self._generate_speeds()


    def _generate_speeds(self):
        for i in range(len(self.path) - 1):
            x1, y1 = self.path[i]
            x2, y2 = self.path[i + 1]
            dx = (x2 - x1)
            dy = (y2 - y1)
            dist = sqrt(dx**2 + dy**2)
            dx = dx * self.config["run"]["speed"]/dist
            dy = dy * self.config["run"]["speed"]/dist
            self.speeds.append((dx, dy))

    def load_path(self, filename):
        """Load the path from a JSON file."""
        try:
            with open(filename, "r") as f:
                return [(x, y) for x, y in json.load(f)]
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.log.error(f"Error loading path file: {e}")
            return []

    def start(self):
        """Follow the path by sending speed commands."""
        while True:
            for x, y in self.speeds:
                time.sleep(self.config["run"]["instruction_delay"])
                self.sendSpeedCart(x, y, 0)
