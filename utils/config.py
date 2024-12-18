from utils.tools import load_yml
from sys import exit

class Config:
    _instance = None
    def __new__(cls, config=None):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            try:
                cls._instance.config = load_yml(
                    "config.yml"
                )  # config.yml must be in the root folder of the project
            except FileNotFoundError as e:
                print(
                    f"Error: {e}\nEnsure 'config.yml' is in the root folder of the project."
                )
                exit(1)
        return cls._instance

    def get(self):
        return self.config


if __name__ == "__main__":

    # Create an instance of Config
    config_instance = Config()  # This will trigger the singleton behavior
    config = config_instance.get()  # Now you can access the config through the instance

    print(config)  # Example of using the config