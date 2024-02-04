import logging
import os
from datetime import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

LOGGING_NAME = 'info.log'
LOGGING_DIR = BASE_DIR / 'logs'
LOGGING_PATH = LOGGING_DIR / LOGGING_NAME

LOGGING_CONF = dict(
    version=1,
    disable_existing_loggers=False,
    formatters={
        'f': {
            'format':
                '%(asctime)s %(name)s:%(lineno)5s %(levelname)s:%(message)s',
        },
    },
    handlers={
        'h': {
            'level': logging.INFO,
            'formatter': 'f',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': LOGGING_PATH,
            'when': 'midnight',
            'atTime': time(0, 0),
            'interval': 1,
            'backupCount': 10,
        },
    },
    loggers={
        None: {
            'handlers': ['h'],
            'level': logging.INFO,
        },
    },
)


if not os.path.exists(LOGGING_DIR):
    os.makedirs(LOGGING_DIR)
