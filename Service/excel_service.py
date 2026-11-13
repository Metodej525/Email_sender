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
                 selected_sheet: str,
                 app_state: AppStateProtocol,
                 ) -> None:
        # Uložení závislostí potřebných pro načtení Excelu a aktualizaci stavu aplikace.
        self.excel_raw_load = excel_raw_load
        self.config = config
        self.filepath = config.get(c.EXCEL_SECTION,c.EXCEL_PATH)
        self.selected_sheet = selected_sheet
        self.app_state = app_state

    def excel_load(self) -> None:
        # Načtení aktuální cesty k Excel souboru z konfigurace.
        filepath = self.config.get(c.EXCEL_SECTION,c.EXCEL_PATH)
        try:
            # Načtení vybraného listu a předání výsledného DataFrame do stavu aplikace.
            self.app_state.set_df(self.excel_raw_load(filepath,self.selected_sheet))
            logger.info(f"loaded excel successfully, with selected sheet: {self.selected_sheet}")
        except Exception as e:
            # Zaznamenání chyby a její předání dál, aby ji mohla zpracovat nadřazená část aplikace.
            logger.error(f"failed to load excel with exception: {e}")
            raise


class SheetManager:
    def __init__(self,
                 config: configparser.ConfigParser) -> None:
        # Načtení cesty k Excel souboru a inicializace vybraného listu.
        self.filepath = config.get(c.EXCEL_SECTION, c.EXCEL_PATH)
        self.selected_sheet = None

    def sheet_checker(self) -> tuple[list[str],int]:
        # Otevření Excel souboru a získání názvů všech dostupných listů.
        excel_file = pd.ExcelFile(self.filepath)
        sheets = excel_file.sheet_names
        logger.debug(f"checked sheets: {sheets}, total: {len(sheets)}")
        # Vrácení seznamu listů a jejich celkového počtu.
        return sheets, len(sheets)

    # def selected_sheet_index(self):
    #     if not self.selected_sheet:
    #         self.selected_sheet = 0
    #     sheets, _ = self.sheet_checker()
    #     logger.debug(f"selected sheet is: {self.selected_sheet}")
    #     return sheets[self.selected_sheet]

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
                 ) -> list[tuple] | list[None]:
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
                    path: str,
                    safe_write_config: Callable[[configparser.ConfigParser, str], None],
                    ) -> None:
    # Kontrola, zda konfigurace obsahuje sekci EXCEL.
    if c.EXCEL_SECTION not in config:
        raise ValueError("Chybí sekce EXCEL")

    # Pokud je zadaná cesta stejná jako cesta v konfiguraci, není potřeba nic měnit.
    if path == config.get(c.EXCEL_SECTION,c.EXCEL_PATH):
        logger.debug('given path and path in config are the same')
        return

    # Uložení nové cesty k Excel souboru do konfigurace.
    config.set(c.EXCEL_SECTION, c.EXCEL_PATH, path)

    # Bezpečný zápis aktualizované konfigurace do konfiguračního souboru.
    safe_write_config(config, c.CONFIG_PATH)
    logger.debug(f"reloaded excel path: {path}")