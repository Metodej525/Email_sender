from typing import Any

import constants as c
import pandas as pd
import configparser
import logging

from core.protocols import AppStateProtocol
from core.utilities import remove_diacritics
from pathlib import Path
from collections.abc import Callable

logger = logging.getLogger(__name__)

class ExcelLoader:
    def __init__(self,config: configparser.ConfigParser,
                 excel_raw_load: Callable[[str | Path ,str],pd.DataFrame],
                 app_state: AppStateProtocol,
                 ) -> None:
        # Uložení závislostí potřebných pro načtení Excelu a aktualizaci stavu aplikace.
        self.excel_raw_load = excel_raw_load
        self.config = config
        self.app_state = app_state

    def initial_excel_load(self,first_path: str, sheet_list: list[str]) -> None:
        # Načte první list Excelu

            self.excel_load(first_path,sheet_list[0])

    def excel_load(self,
                   path: str,
                   sheet: str,
                   ) -> None:

        try:
            # Načtení vybraného listu a předání výsledného DataFrame do stavu aplikace.
            self.app_state.set_df(self.excel_raw_load(path,sheet))
            logger.info(f"loaded excel successfully, with selected sheet: {sheet}")

        except Exception as e:
            # Zaznamenání chyby a její předání dál, aby ji mohla zpracovat nadřazená část aplikace.

            logger.error(f"failed to load excel with exception: {e}")
            raise

def _excel_path_checker(config:configparser.ConfigParser) -> dict[str,str]:
    # vrátí hodnoty v sekci EXCEL_PATH_SECTION a jejich počet

    excel_path_dict = dict(config["EXCEL_PATHS"])

    return excel_path_dict

def _excel_path_validator(
                          raw_path_dict: dict[str,str],
                          ) -> tuple[dict[Any, Any] | None, int | None]:
    # validuje cesty v EXCEL_PATH_SECTION, odstraní ze slovníku None hodnoty a upraví jejich počet

    path_dict = {}
    number_of_paths = len(raw_path_dict)
    raw_number_of_paths = len(raw_path_dict)

    if number_of_paths == 0:
        logger.debug("found no set paths in EXCEL_PATH_SECTION")
        return None,None

    for path, value in raw_path_dict.items():
        if value:
            path_dict[path] = value
        else:
            number_of_paths -= 1

    if number_of_paths == 0:
        logger.debug("found no set paths in EXCEL_PATH_SECTION by filtering")
        return None,None

    logger.debug(f"filtered excel paths from {raw_number_of_paths} to {number_of_paths}")
    return path_dict, number_of_paths

def get_excel_path_status(config:configparser.ConfigParser
                          ) -> dict[Any, Any] | None:
    # Zavolá validaci cest k excelům, vrátí výsledné hodnoty

    excel_path_dict = _excel_path_checker(config)
    path_dict, number_of_paths = _excel_path_validator(excel_path_dict)

    if path_dict is None or number_of_paths is None:
        logger.debug("Failed to load excel paths from EXCEL_PATH_SECTION")
        return None
    else:
        return path_dict

class SheetManager:
    def __init__(self,
                 key_path: str,
                 config: configparser.ConfigParser) -> None:
        # Načtení cesty k Excel souboru a inicializace vybraného listu.
        self.filepath = config.get(c.EXCEL_PATHS, key_path)
        self.selected_sheet = None

    def sheet_checker(self) -> tuple[list[str],int]:
        # Otevření Excel souboru a získání názvů všech dostupných listů.
        excel_file = pd.ExcelFile(self.filepath)
        sheets = excel_file.sheet_names
        logger.debug(f"checked sheets: {sheets}, total: {len(sheets)}")
        # Vrácení seznamu listů a jejich celkového počtu.
        return sheets, len(sheets)

def initial_filter(df: pd.DataFrame) -> pd.DataFrame:
    """Vyfiltruje certifikáty typu Q-TW-CZ a vyřadí záznamy s ukončeným PPV."""
    # Uložení počtu řádků před filtrováním pro následné porovnání.
    before_count = len(df)

    # Zachování pouze záznamů, které splňují obě podmínky:
    # typ certifikátu je Q-TW-CZ a termín není ukončen ppv.
    df = df[
        (
            df['Typ cert.']
            .fillna('')
            .str.strip()
            .eq('Q-TW-CZ')
        )
        &
        (
            df['Termín']
            .fillna('')
            .str.strip()
            .ne('ukončen ppv')
        )
        ]
    # Zjištění počtu řádků po filtrování.
    after_count = len(df)

    logger.debug(f"Initial filter applied: {before_count} -> {after_count} rows")

    logger.info("Initial dataframe filter completed")
    return df

def excel_search(value: str,
                 df: pd.DataFrame | None
                 ) -> list[tuple]:
    # Vyhledávání probíhá pouze tehdy, pokud je DataFrame k dispozici.
    if df is not None:
        # Nejprve hledání podle loginu bez ohledu na velikost písmen a diakritiku.
        # Výsledky jsou zbaveny duplicit a omezeny na prvních 5 záznamů.
        slice_df = df[df['Login'].apply(remove_diacritics).str.lower().str.startswith(value, na=False)].drop_duplicates().head(5)

        if slice_df.empty:
            # Pokud nebyl nalezen login, hledání pokračuje podle příjmení.
            slice_df = df[df['Příjmení'].apply(remove_diacritics).str.lower().str.startswith(remove_diacritics(value),
                                                                                             na=False)].drop_duplicates().head(
                5)
            if slice_df.empty:
                # Pokud nebylo nalezeno příjmení, hledání pokračuje podle jména.
                slice_df = df[df['Jméno'].apply(remove_diacritics).str.lower().str.startswith(remove_diacritics(value),
                                                                                                 na=False)].drop_duplicates().head(
                    5)

        # Převod vybraných sloupců na seznam n-tic pro další zpracování.
        return list(zip(
                        slice_df['Příjmení'],
                        slice_df['Jméno'],
                        slice_df['Login'],
                        slice_df['Typ cert.'],
                        slice_df['Platnost do'],))
    # Pokud DataFrame není dostupný, vrátí se prázdný seznam.

    return []

def excel_path_load(config: configparser.ConfigParser,
                    path_key: str,
                    path_value: str,
                    sheet: str,
                    safe_write_config: Callable[[configparser.ConfigParser, str], None],
                    excel_load: Callable[[str, str], None],
                    app_state:AppStateProtocol,
                    ) -> None:

    # Kontrola, zda konfigurace obsahuje sekci EXCEL.
    if c.EXCEL_PATHS not in config:
        raise ValueError("Config section is missing: EXCEL_PATHS")

    # Pokud je zadaná cesta stejná jako cesta v konfiguraci, není potřeba nic měnit.
    if path_value == config.get(c.EXCEL_PATHS, path_key):
        excel_load(path_value, sheet)
        logger.debug(f'given path {path_value} and path in config are the same')
        return

    # Uložení nové cesty k Excel souboru do konfigurace.
    config.set(c.EXCEL_PATHS, path_key, path_value)

    # Nastaví aktuální cestu k souboru v AppState
    app_state.set_file_path(path_key,path_value)

    # Bezpečný zápis aktualizované konfigurace do konfiguračního souboru.
    safe_write_config(config, c.CONFIG_PATH)
    logger.debug(f"reloaded excel path: {path_value}")