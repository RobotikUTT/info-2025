from utils.log import Log
from utils.config import Config
from utils.tools import load_yml

class Strategy():
    def __init__(self):
        self.log = Log("Strategy")
        self.config = Config().get()
        self.strategy = load_yml(self.config["strategy"]["path"])
        self.map = load_yml(self.config["run"]["map_file"])

        self.ordered_points = []
        for point_name in self.strategy:
            point = next((p for p in self.map if p["name"] == point_name), None)
            if point:
                self.ordered_points.append(point)
            else:
                self.log.error(f"⚠️ Point '{point_name}' introuvable dans la map !")

    def wait_for_signal(self, point_name: str):
        self.log.info(f"Waiting to go to: {point_name}")
        input("↪️  Appuie sur Entrée pour envoyer le robot...")  # À remplacer par un signal plus tard


    def start(self, path_follower):
        for point in self.ordered_points:
            self.wait_for_signal(point["name"])
            path_follower.run_to_point(point)