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
    """
    Formátuje logovací záznamy do strukturovaného JSON formátu.
    Pro záznamy úrovně DEBUG doplňuje diagnostická metadata.
    """

    def format(self, record: logging.LogRecord) -> str:
        # Základní struktura logovacího záznamu
        data = {
            "time": self.formatTime(record, "%Y-%m-%d %H:%M:%S"),
            "hostname": HOSTNAME,
            "level": record.levelname,
            "message": record.getMessage(),
        }

        # U DEBUG záznamů doplňuje informace o původu logovací zprávy,
        # které usnadňují diagnostiku a vyhledávání chyb.
        if record.levelno == logging.DEBUG:
            data.update({
                "logger": record.name,
                "file": record.filename,
                "line": record.lineno,
                "function": record.funcName,
            })
        # Serializuje připravená data do JSON řetězce.
        return json.dumps(data)
def setup_logger() -> logging.Logger:
    # Ověřuje jestli logger existuje
    logger = logging.getLogger()
    if logger.handlers:
        return logger

    # Ověřuje pro složku root/logs , pokud ne vytvoří ji
    Path(c.LOG_PATH).parent.mkdir(parents=True, exist_ok=True)

    # TimedRotatingFileHandler:
    # - rotuje logs každý den o půlnoci (při dalším zápisu)
    # - uchovává max 10 rotovaných souborů
    # - starší soubory smaže
    # - suffix určuje formát data v názvu rotovaných souborů
    timed_handler = ConcurrentTimedRotatingFileHandler(filename=c.LOG_PATH,
                                                       when='midnight',
                                                       backupCount=10,
                                                       encoding='utf-8')
    timed_handler.suffix = "%Y%m%d"

    # Nastavení logger handlerů
    timed_handler.setFormatter(PrettyJsonFormatter())
    logger.addHandler(timed_handler)

    # Nastavení logs level
    logger.setLevel(logging.INFO)
    logger.debug("logger set")
    return logger

def setup_config() -> configparser.ConfigParser:
    # Určuje základní adresář aplikace podle způsobu jejího spuštění.
    # Při spuštění jako samostatný executable se použije umístění
    # spustitelného souboru, jinak se využije výchozí adresář projektu.
    if getattr(sys, 'frozen', False):
        BASE_DIR = Path(os.path.dirname(sys.executable))
    else:
        BASE_DIR = c.BASE_DIR

    # Sestavuje absolutní cestu ke konfiguračnímu souboru
    # na základě základního adresáře aplikace.
    CONFIG_PATH = BASE_DIR / c.CONFIG_PATH

    # Inicializuje parser pro načítání INI konfigurace.
    config = configparser.ConfigParser()

    # Ověřuje existenci konfiguračního souboru.
    # Pokud soubor není dostupný, zaznamená chybu a vrátí
    # prázdnou konfiguraci.
    if not CONFIG_PATH.exists():
        logger.error("Config file not found")
        return config

    try:
        # Načítá konfiguraci s nastaveným kódováním.
        config.read(filenames=CONFIG_PATH, encoding=c.CONFIG_ENCODING)

        # Zaznamenává úspěšné načtení konfiguračního souboru.
        logger.info(f"Config loaded with {CONFIG_PATH}")

    # Zachycuje chyby vzniklé při parsování INI souboru.
    except configparser.ParsingError as e:
        logger.error(f"Config failed parsing with exception: {e}")

    return config