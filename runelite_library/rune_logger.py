import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from config import settings

# Create logs directory if not exists
LOG_DIR = Path("utils")
LOG_DIR.mkdir(exist_ok=True)

# File paths
ACTIVITY_LOG_PATH = LOG_DIR / "main.log"


LOGGING_LEVEL = logging.DEBUG if settings.debug else logging.INFO


def setup_logger(name, log_file, level=LOGGING_LEVEL, formatter=None):
    """Creates and returns a logger with rotation."""
    handler = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=3)
    if not formatter:
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.hasHandlers():
        logger.addHandler(handler)

    logger.propagate = False
    return logger


# Activity logger for detailed troubleshooting
activity_logger = setup_logger("activity_logger", ACTIVITY_LOG_PATH)


def log_event(message: str, level="info"):
    """
    Log a generic event to activity.log.

    message: a string that is descriptive of the event being logged

    level: "debug", "info", "warning", "error", "critical"
    """
    getattr(activity_logger, level.lower())(message)
