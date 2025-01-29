import logging
from utils.config import Config, LoggerConfig


class ColorFormatter(logging.Formatter):
    """A formatter that changes the background color according to the log level."""
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

    def format(self, record: logging.LogRecord) -> str:
        log_color = self.COLORS.get(record.levelno, self.reset)
        fmt = (
            f"{{asctime}} {log_color}{{levelname:<8}}{self.reset} "
            f"{self.bold}{{name}}{self.reset} {{message}}"
        )
        formatter = logging.Formatter(fmt, "%Y-%m-%d %H:%M:%S", style="{")
        return formatter.format(record)


class PlainFormatter(logging.Formatter):
    def __init__(self):
        super().__init__(
            "{asctime} - {levelname} - {name} - {message}",
            "%Y-%m-%d %H:%M:%S",
            style="{",
        )


def setup_logging(loggers: list[LoggerConfig] | None = None):
    """Setup"""
    if not loggers:
        loggers = Config().loggers
    for logger_conf in loggers:
        logger = logging.getLogger(logger_conf.name)

        file_handler = logging.FileHandler(logger_conf.path)
        file_handler.setLevel(logger_conf.level)
        file_handler.setFormatter(PlainFormatter())
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logger_conf.level)
        console_handler.setFormatter(ColorFormatter())
        logger.addHandler(console_handler)
