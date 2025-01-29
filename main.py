from utils.config import Config
from utils.log import setup_logging


def main():
    settings = Config()
    setup_logging(settings.loggers)


if __name__ == "__main__":
    main()
