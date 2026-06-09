import json
import logging
from concurrent_log_handler import ConcurrentTimedRotatingFileHandler

import configparser
import os
import sys
from pathlib import Path

import constants as c

import socket

HOSTNAME = socket.gethostname()

logger = logging.getLogger(__name__)

class PrettyJsonFormatter(logging.Formatter):
    """nastaven formátu logů
    pro level Debug a pro zbytek
    """

    def format(self, record):

        data = {
            "time": self.formatTime(record, "%Y-%m-%d %H:%M:%S"),
            "hostname": HOSTNAME,
            "level": record.levelname,
            "message": record.getMessage(),
        }

        # DEBUG a vyšší → přidej debug metadata
        if record.levelno == logging.DEBUG:
            data.update({
                "logger": record.name,
                "file": record.filename,
                "line": record.lineno,
                "function": record.funcName,
            })

        return json.dumps(data)
def setup_logger():
    #check jestli logger existuje
    logger = logging.getLogger()
    if logger.handlers:
        return logger
    #check pro složku root/logs , pokud ne vytvoří ji
    Path(c.LOG_PATH).parent.mkdir(parents=True, exist_ok=True)

    # TimedRotatingFileHandler:
    # - rotuje logs každý den o půlnoci (při dalším zápisu)
    # - uchovává max 10 rotovaných souborů
    # - starší soubory smaže
    # - suffix určuje formát data v názvu rotovaných souborů
    timed_handler = ConcurrentTimedRotatingFileHandler(filename=c.LOG_PATH,when='midnight',backupCount=10,encoding='utf-8')
    timed_handler.suffix = "%Y%m%d"

    #set handlerů
    timed_handler.setFormatter(PrettyJsonFormatter())
    logger.addHandler(timed_handler)
    #set logs level
    logger.setLevel(logging.DEBUG)
    logger.debug("logger set")
    return logger

def setup_config():
    if getattr(sys, 'frozen', False):
        BASE_DIR = Path(os.path.dirname(sys.executable))
    else:
        BASE_DIR = c.BASE_DIR

    CONFIG_PATH = BASE_DIR / c.CONFIG_PATH

    config = configparser.ConfigParser()
    if not CONFIG_PATH.exists():
        logger.error("Config file not found")
    try:
        config.read(filenames=CONFIG_PATH, encoding=c.CONFIG_ENCODING)
        logger.info(f"Config loaded with {CONFIG_PATH}")
    except configparser.ParsingError as e:
        logger.error(f"Config failed parsing with exception: {e}")
    return config