from utils.log import Log
from utils.config import Config
from utils.tools import load_yml
from threading import Thread
from queue import Queue
import time
import modules.strategy.structure_validator as structure_validator

class Strategy(Thread):
    def __init__(self, position_controller, effector_controller):
        super().__init__()
        self.log = Log("Strategy")
        self.config = Config().get()
        self.strategy = load_yml(self.config["strategy"]["path"])
        self.map = load_yml(self.config["run"]["map_file"])

        if not structure_validator.verify(self.strategy):
            raise Exception("Bad strategy format")

        self.position_controller = position_controller
        self.effector_controller = effector_controller

        self.current_step = 0

        self.step_queue = Queue()

    def run(self):
        while True:
            step = self.step_queue.get()
            if step:
                self.redirect(step)

    def move_named(self, name):
        self.log.info(f"move_named to {name}")
        if name in self.map:
            pos = self.map[name]
            self.move_absolute(pos['x'], pos['y'], pos['w'])

    def move_absolute(self, x, y, w):
        self.log.info(f"move_absolute to x:{x}, y:{y}, w:{w}")
        self.position_controller.goTo(x, y, w, self.nextStep)

    def move_relative(self, x, y, w):
        self.log.info(f"move_delta by x:{x}, y:{y}, w:{w}")
        self.position_controller.goToRelative(x, y, w, self.nextStep)

    def effect_take(self, ids):
        self.log.info(f"effect_take ids: {ids}")
        for id in ids:
            self.effector_controller.magnetize(id)
        self.nextStep()

    def effect_release(self, ids):
        self.log.info(f"effect_release ids: {ids}")
        for id in ids:
            self.effector_controller.demagnetize(id)
        self.nextStep()

    def wait(self, duration):
        self.log.info(f"wait for {duration} seconds")
        time.sleep(duration)
        self.nextStep()

    def nextStep(self):
        self.current_step += 1
        if self.current_step < len(self.strategy):
            step = self.strategy[self.current_step]
            self.step_queue.put(step)
        else:
            self.log.info("Stratégie terminée.")

    def redirect(self, step):
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
            if "take" in effect:
                self.effect_take(effect["take"])
            if "release" in effect:
                self.effect_release(effect["release"])
        elif "wait" in step:
            self.wait(step["wait"])
        else:
            self.log.warn(f"Étape inconnue ou non gérée : {step}")
