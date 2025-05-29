from modules.communication.speed_communication import SpeedCommunication
from pathlib import Path
from utils.config import Config
from utils.log import Log
import math
from utils.tools import load_yml
import time
import threading

class PathFollower(SpeedCommunication):
    # Hérite de SpeedCommunication pour l'envoi des vitesse
    def __init__(self, detect_service):
        super().__init__()  # super().__init__(detect_service) était cassé Guilpy
        self.config = Config().get()
        self.log = Log("PathFollower")
        self.detection_service = detect_service
        path_obj = Path(self.config["run"]["map_file"])
        filename = path_obj.resolve()


        self.map = load_yml(filename)

        self.points = {}
        self.position = {'x': self.config["run"]["position"]["x"], 'y':self.config["run"]["position"]["y"], 'r': self.config["run"]["position"]["r"]}
        self._generate_speeds()

        # Gestion détection
        self.interrupted = False
        self.lock = threading.Lock()
        self.detection_thread = threading.Thread(target=self.handle_detection, daemon=True)
        self.detection_thread.start()


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

    def update_position(self, x_rel: float, y_rel: float, r_rel: float) -> None:
        """Update the absolute position of the robot by adding relative position"""
        self.position['x'] += x_rel
        self.position['y'] += y_rel
        self.position['r'] += r_rel

    def handle_detection(self):
        while not self.interrupted:
            if self.detection_service and self.detection_service.stop:
                self.interrupted = True
                self.log.warn("Obstacle détecté ! Envoi d'un STOP d'urgence.")
                self.sendSpeedCart(-1, -1, -1, 0)  # STOP immédiat
                break
            time.sleep(0.05)  # Surveillance rapide mais non bloquante

    def run_to(self, point_name: str):
        self.log.debug(f"Follow path: {self.points[point_name]=}")
        x, y, r, _ = self.points[point_name]
        x, y, r = self.relative_from_absolute(x, y, r)

        with self.lock:
            self.interrupted = False  # Reset avant chaque mouvement

        # ====== ESSAI D'envoi d'interruption =======
        # NE PAS DELETE LE CODE SUIVANT
        # Envoi d'un STOP immédiat pour tester l'interruption
        """
        self.log.info("Envoi d'une commande STOP pour test d'interruption.")
        self.sendSpeedCart(-1, -1, -1, 0)
        time.sleep(0.1)  # petite pause pour laisser passer le STOP
        """
        # ====== FIN ESSAI D'envoi d'interruption =======

        self.log.info(f"Sending x={x}, y={y}, r={r}")
        self.sendSpeedCart(int(x), int(y), int(r), 0)

        # Simulation d'attente du mouvement (remplacer par logique réelle plus tard)
        t0 = time.time()
        while time.time() - t0 < self.config["run"]["instruction_delay"]:  # e.g. 2 sec
            with self.lock:
                if self.interrupted:
                    self.log.warn("Mouvement interrompu par un obstacle.")
                    self.sendSpeedCart(-1, -1, -1, 0)

                    return
            time.sleep(0.05)

        self.update_position(x, y, r)



    def follow_path(self):
        # TODO : need to be implemented by Guilpy
        # interface pour le moment
        self.run_to("test_ligne_x50")
