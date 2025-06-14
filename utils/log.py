import logging
from cysystemd import journal
from utils.config import Config


class LoggingFormatter(logging.Formatter):
    # Colors and styles
    black = "\x1b[30m"
    red = "\x1b[31m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    blue = "\x1b[34m"
    gray = "\x1b[38m"
    reset = "\x1b[0m"
    bold = "\x1b[1m"

    COLORS = {
        logging.DEBUG: gray + bold,
        logging.INFO: blue + bold,
        logging.WARNING: yellow + bold,
        logging.ERROR: red,
        logging.CRITICAL: red + bold,
    }

    def format(self, record: object) -> str:
        log_color = self.COLORS.get(record.levelno, self.reset)
        format = "(black){asctime}(reset) (levelcolor){levelname:<8}(reset) (green){name}(reset) {message}"
        format = format.replace(
            "(black)", self.bold
        )  # removed 'self.black +' because can't be seen in terminal
        format = format.replace("(reset)", self.reset)
        format = format.replace("(levelcolor)", log_color)
        format = format.replace("(green)", self.green + self.bold)
        formatter = logging.Formatter(format, "%Y-%m-%d %H:%M:%S", style="{")
        return formatter.format(record)


class PlainFormatter(logging.Formatter):
    def __init__(self):
        super().__init__(
            "%(asctime)s - %(levelname)s - %(name)s - %(message)s", "%Y-%m-%d %H:%M:%S"
        )


class Log(object):
    def __init__(self, name: str):
        """
        Log handler
        Parameters
        ----------
        name : String, name of the module
        config_ : config object containing all application parameters
        """
        self.name = name
        self.config = Config().get()
        self.path = self.config["log"]["path"]
        self.level = self.config["log"]["level"]

        if self.name not in self.config["log"]["logger"].keys():
            # Add a custom formatter
            logging._defaultFormatter = logging.Formatter("%(message)s")
            logger = logging.getLogger(self.name)
            log_level = getattr(
                logging, self.config["log"]["level"], logging.INFO
            )  # If can't extract, default to INFO level
            logger.setLevel(log_level)

            # Create formatters
            color_formatter = LoggingFormatter()
            plain_formatter = PlainFormatter()

            # Stream handler
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.DEBUG)
            stream_handler.setFormatter(color_formatter)

            # File handler
            file_handler = logging.FileHandler(self.path)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(plain_formatter)

            # Journal handler
            journal_handler = journal.JournaldLogHandler()
            journal_handler.setLevel(logging.DEBUG)
            journal_handler.setFormatter(plain_formatter)

            # Add handlers
            if "stream" in self.config["log"]["mode"]:
                logger.addHandler(stream_handler)

            if "file" in self.config["log"]["mode"]:
                logger.addHandler(file_handler)

            if "journal" in self.config["log"]["mode"]:
                logger.addHandler(journal_handler)

            # Add the logger to the config file
            self.config["log"]["logger"][self.name] = logger

    def info(self, message: str):
        """
        Log info message
        Parameters
        ----------
        message : String, message to log
        """
        self.config["log"]["logger"][self.name].info(message)

    def debug(self, message: str):
        """
        Log debug message
        Parameters
        ----------
        message : String, message to log
        """
        self.config["log"]["logger"][self.name].debug(message)

    def warn(self, message: str):
        """
        Log warning message
        Parameters
        ----------
        message : String, message to log
        """
        self.config["log"]["logger"][self.name].warning(message)

    def error(self, message: str, exception=None):
        """
        Log error message
        Parameters
        ----------
        message : String, message to log
        exception : Exception, exception to log
        """
        if exception is not None:
            self.config["log"]["logger"][self.name].error(
                f"{message} - {type(exception).__name__} - {str(exception)}"
            )
        else:
            self.config["log"]["logger"][self.name].error(message)


if __name__ == "__main__":
    log = Log("TestPlugin")
    log.info("info message")
    log.debug("debug message")
    log.warn("warning message")
    log.error("error message")
