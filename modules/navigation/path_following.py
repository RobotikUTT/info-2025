import json
import time
from modules.communication.speed_communication import SpeedCommunication

class PathFollower(SpeedCommunication):
    def __init__(self, detect_service, filename="../../ressources/path/path.json", scale=1):
        super().__init__(detect_service)
        self.scale = scale
        self.path = self.load_path(filename)

        self.speeds = []
        for i in range(len(self.path) - 1):
            x1, y1 = self.path[i]
            x2, y2 = self.path[i + 1]
            dx = (x2 - x1) * self.scale
            dy = (y2 - y1) * self.scale
            self.speeds.append((dx, dy))

    def load_path(self, filename):
        """Load the path from a JSON file."""
        try:
            with open(filename, "r") as f:
                return [(x, y) for x, y in json.load(f)]
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading path file: {e}")
            return []

    def start(self):
        """Follow the path by sending speed commands."""
        for x, y in self.speeds:
            time.sleep(0.1)
            self.sendSpeedCart(x, y, 0)
