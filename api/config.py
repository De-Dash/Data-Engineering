import os
import sys
import pathlib
import logging
from logging.handlers import TimedRotatingFileHandler


PACKAGE_ROOT = pathlib.Path(__file__).resolve().parent.parent

FORMATTER = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s-"
        "%(funcName)s - %(lineno)d - %(message)s")

LOG_DIR = PACKAGE_ROOT/'logs'
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR/'api.log'


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SERVER_PORT = 8000


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


def get_logger(*, logger_name:str):
    """
    Get logger with prepared handlers.
    """
    logger = logging.getLogger(logger_name)

    logger.setLevel(logging.DEBUG)

    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    logger.propagate = False

    return logger

def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    console_handler.setLevel(logging.DEBUG)
    return console_handler


def get_file_handler():
    file_handler = TimedRotatingFileHandler(
            LOG_FILE, when='midnight')
    file_handler.setFormatter(FORMATTER)
    file_handler.setLevel(logging.WARNING)
    return file_handler
