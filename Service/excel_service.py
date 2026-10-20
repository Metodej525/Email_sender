import constants as c
import pandas as pd
from core.utilities import remove_diacritics
import logging

logger = logging.getLogger(__name__)

class ExcelLoader:
    def __init__(self,config, excel_raw_load, selected_sheet,app_state):
        self.excel_raw_load = excel_raw_load
        self.config = config
        self.filepath = config.get(c.EXCEL_SECTION,c.EXCEL_PATH)
        self.selected_sheet = selected_sheet
        self.app_state = app_state

    def excel_load(self):
        filepath = self.config.get(c.EXCEL_SECTION,c.EXCEL_PATH)
        try:
            self.app_state.set_df(self.excel_raw_load(filepath,self.selected_sheet))
            logger.info(f"loaded excel successfully, with selected sheet: {self.selected_sheet}")
        except Exception as e:
            logger.error(f"failed to load excel with exception: {e}")
            raise


class SheetManager:
    def __init__(self,config):
        self.filepath = config.get(c.EXCEL_SECTION, c.EXCEL_PATH)
        self.selected_sheet = None

    def sheet_checker(self):
        excel_file = pd.ExcelFile(self.filepath)
        sheets = excel_file.sheet_names
        logger.debug(f"checked sheets: {sheets}, total: {len(sheets)}")
        return sheets, len(sheets)

    def selected_sheet(self):
        if not self.selected_sheet:
            self.selected_sheet = 0
        sheets = self.sheet_checker()
        logger.debug(f"selected sheet is: {self.selected_sheet}")
        return sheets[self.selected_sheet]

def initial_filter(df):
    """vyfiltruje jen certifikáty typu Q-TW-CZ + všechny kromě ukončených v pp"""
    before_count = len(df)
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
    after_count = len(df)

    logger.debug(f"Initial filter applied: {before_count} -> {after_count} rows")

    logger.info("Initial dataframe filter completed")
    return df

def excel_search(value,df):
    if df is not None:
        slice_df = df[df['Login'].apply(remove_diacritics).str.lower().str.startswith(value, na=False)].drop_duplicates().head(5)
        if slice_df.empty:
            slice_df = df[df['Příjmení'].apply(remove_diacritics).str.lower().str.startswith(value,
                                                                                             na=False)].drop_duplicates().head(
                5)
            if slice_df.empty:
                slice_df = df[df['Jméno'].apply(remove_diacritics).str.lower().str.startswith(value,
                                                                                                 na=False)].drop_duplicates().head(
                    5)
        return list(zip(
                        slice_df['Příjmení'],
                        slice_df['Jméno'],
                        slice_df['Login'],
                        slice_df['Typ cert.'],
                        slice_df['Platnost do'],))
    return []

def excel_path_load(config,path,safe_write_config):
    if c.EXCEL_SECTION not in config:
        raise ValueError("Chybí sekce EXCEL")
    if path == config.get(c.EXCEL_SECTION,c.EXCEL_PATH):
        logger.debug('given path and path in config are the same')
        return
    config.set(c.EXCEL_SECTION, c.EXCEL_PATH, path)
    safe_write_config(config, c.CONFIG_PATH)
    logger.debug(f"reloaded excel path: {path}")