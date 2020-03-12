import os
import sys
import pathlib
import logging
from logging.handlers import TimedRotatingFileHandler


PACKAGE_ROOT = pathlib.Path(__file__).resolve().parent.parent

FORMATTER = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s-"
        "%(funcName)s:%(lineno)d - %(message)s")

LOG_DIR = PACKAGE_ROOT/'logs'
LOG_DIR.mkdir(exist_okay=True)
LOG_FILE = LOG_DIR/'api.log'


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = TRUE
    SERVER_PORT = 8000


class DevelopmentConfig(Config):
    DEVELOPMENT = TRUE
    DEBUG = TRUE
