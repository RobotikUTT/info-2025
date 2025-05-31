from utils.log import Log
from utils.config import Config
from utils.tools import load_yml
from threading import Thread
from queue import Queue
import time
import modules.strategy.structure_validator as structure_validator
from utils.position import Position

class Strategy(Thread):
    def __init__(self, position_controller, effector_controller, jaune=True):
        super().__init__()
        self.log = Log("Strategy")
        self.config = Config().get()
        self.strategy = load_yml(self.config["strategy"]["path"]["jaune" if jaune else "bleu"])
        self.log.info(f"Stratégie chargée : {self.strategy}")
        color = "jaune" if jaune else "bleu"
        filename = f"{self.config['run']['map_file']}_{color}.yml"
        self.map = load_yml(filename)
        self.log.info(f"Map chargée : {self.map}")

        if not structure_validator.verify(self.strategy):
            raise Exception("Bad strategy format")

        self.position_controller = position_controller
        self.effector_controller = effector_controller

        self.current_step = 0

        self.step_queue = Queue()

        self.step_queue.put(self.strategy[0])

    def run(self):
        while True:
            self.log.info("Running strat")
            step = self.step_queue.get()
            if step:
                self.redirect(step)

    def move_named(self, name):
        self.log.info(f"move_named to {name}")
        for i in self.map:
            if name == i["name"]:
                self.move_absolute(i['x'], i['y'], i['r'])
                return
        self.nextStep()

    def move_absolute(self, x, y, w):
        self.log.info(f"move_absolute to x:{x}, y:{y}, w:{w}")
        self.position_controller.goTo(x, y, w, self.nextStep)

    def move_relative(self, x, y, w):
        self.log.info(f"move_delta by x:{x}, y:{y}, w:{w}")
        self.position_controller.goToRelative(x, y, w, self.nextStep)

    def wait(self, duration):
        self.log.info(f"wait for {duration} seconds")
        self.position_controller.speedCommunication.sendSpeedCart(0, 0, 0)
        time.sleep(duration)
        self.nextStep()

    def nextStep(self):
        self.current_step += 1
        if self.current_step < len(self.strategy):
            step = self.strategy[self.current_step]
            self.step_queue.put(step)
        else:
            self.log.info("Stratégie terminée.")

    def set_pos(self, x, y, w):
        self.log.info(f"set_pos by x:{x}, y:{y}, w:{w}")
        self.position_controller.positionTracker.setCurrentPosition(Position(x, y, w))
        self.nextStep()

    def redirect(self, step):
        self.log.info(f"strategy step : {step}")
        if "move" in step:
            move = step["move"]
            move_type = move.get("type")
            if move_type == "named":
                self.move_named(move["target"])
            elif move_type == "absolute":
                self.move_absolute(move["x"], move["y"], move["w"])
            elif move_type == "relative":
                self.move_relative(move["x"], move["y"], move["w"])
            else:
                self.log.error(f"Type de mouvement inconnu : {move_type}")

        elif "effect" in step:
            effect = step["effect"]
            if effect == "set_banner_close":
                self.effector_controller.set_banner_close()
            elif effect == "set_banner_open":
                self.effector_controller.set_banner_open()
            elif effect == "take_everything":
                self.effector_controller.take_everything()
            elif effect == "put_down_everything":
                self.effector_controller.put_down_everything()
            else:
                print(f"⚠️ Effet inconnu : {effect}")
            self.nextStep()
        elif "wait" in step:
            self.wait(step["wait"])

        elif "set_pos" in step:
            pos = step["set_pos"]
            self.set_pos(pos["x"], pos["y"], pos["w"])


        else:
            self.log.warn(f"Étape inconnue ou non gérée : {step}")
