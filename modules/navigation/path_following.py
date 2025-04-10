import json
import time
from modules.communication.speed_communication import SpeedCommunication
from pathlib import Path
from math import sqrt
from utils.config import Config
from utils.log import Log
import math
from utils.tools import load_yml

class PathFollower(SpeedCommunication):
    # Hérite de SpeedCommunication pour l'envoi des vitesse
    def __init__(self, detect_service):
        self.config = Config().get()
        self.log = Log("PathFollower")
        path_obj = Path(self.config["run"]["map_file"])
        filename = path_obj.resolve()

        super().__init__(detect_service)
        self.map = load_yml(filename)

        self.points = {}
        self._generate_speeds()
        self.position = {'x': self.config["run"]["position"]["x"], 'y':self.config["run"]["position"]["y"], 'r': self.config["run"]["position"]["r"]}


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
        for point in self.map :
            x_rel, y_rel, r_rel = self.relative_from_absolute(point['x'], point['y'], point['r'])
            self.points[point["name"]] = (x_rel, y_rel, r_rel, 0.0) # v set à 0 car pas utilisé encore


    def relative_from_absolute(self, x: float, y: float, r: float) -> tuple[float, float, float]:
        # Return relative position target from its absolute one
        dx = x - self.position['x'] # x en mm ?
        dy = y - self.position['y'] # y en mm ?
        dr = r - self.position['r'] # r en deg ?

        theta = math.radians(self.position['r'])
        x_rel = math.cos(theta) * dx + math.sin(theta) * dy
        y_rel = -math.sin(theta) * dx + math.cos(theta) * dy

        return x_rel, y_rel, dr

    def update_postion(self, x_rel: float, y_rel: float, r_rel: float) -> None:
        """Update the absolute position of the robot by adding relative position"""
        self.position['x'] += x_rel
        self.position['y'] += y_rel
        self.position['r'] += r_rel


    def run_to(self, point_name:str):

        """Follow the path by sending speed commands."""
        # self.speeds = [(10.0, 10.0, 0.0, 0.0), (10.0, 5.0, 20.0, 0.0), (0.0, 0.0, 10.0, 0.0)]
        # x, y, d, r avec x,y positions finales en relatif par rapport position actuelle, d la distance, r l'angle robot par rapport à l'actuel
        # while True:
        #    for x, y, r, v in self.points:
                # time.sleep(self.config["run"]["instruction_delay"])
        x, y, r = self.points[point_name] # TODO : check le fonctionnement
        x, y, r = self.relative_from_absolute(x, y, r)
        self.log.info(f"Sending {x=}, {y=}, {r=}, {0.0}")
        # time.sleep(10) # car enverra un msg que quand on veut que le robot bouge
        self.sendSpeedCart(x, y, r, 0.0) # v not used yet
        self.update_postion(x, y, r) # Voir en dynamique selon pos robot
