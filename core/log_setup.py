import json
import logging
from logging.handlers import TimedRotatingFileHandler
import constants as c


def setup_logger():
    logger = logging.getLogger(__name__)

    #upravý formát zápisu logu do .jsnol
    class PrettyJsonFormatter(logging.Formatter):
        def format(self, record):
            data = {
                "time": self.formatTime(record),
                "level": record.levelname,
                "logger": record.name,
                "message": record.getMessage(),
                "file": record.filename,
                "line": record.lineno,
            }
            return json.dumps(data)

    # TimedRotatingFileHandler:
    # - rotuje log každý den o půlnoci (při dalším zápisu)
    # - uchovává max 10 rotovaných souborů
    # - starší soubory smaže
    # - suffix určuje formát data v názvu rotovaných souborů
    timed_handler = logging.handlers.TimedRotatingFileHandler(filename=c.LOG_PATH,when='midnight',backupCount=10,encoding='utf-8')
    timed_handler.suffix = "%Y%m%d"

    #set handlerů
    timed_handler.setFormatter(PrettyJsonFormatter())
    logger.addHandler(timed_handler)
    #set log level
    logger.setLevel(logging.DEBUG)

