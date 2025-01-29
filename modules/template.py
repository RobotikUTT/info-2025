from utils.config import Config
from utils.log import Log


class Template:
    def __init__(self):
        self.config = Config().get()
        self.log = Log("Template")
