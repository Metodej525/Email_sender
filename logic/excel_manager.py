import unicodedata
import constants as c
from Repository.excel_repository import excel_raw_load
def excel_load(config):
    filepath = config.get(c.EXCEL_SECTION,c.EXCEL_PATH)
    try:
        df = excel_raw_load(filepath)
    except Exception as e:
        #zaloguj chybu
        raise
def remove_diacritics(text):
    if not isinstance(text, str):
        return text
    # Normalizace na NFD (rozdělí znaky + diakritiku)
    normalized = unicodedata.normalize('NFD', text)
    # Vrátí jen znaky, které nejsou "Mn" (Mark, Nonspacing = diakritika)
    return ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')
def excel_search(value,df):
    if df is not None:
        slice_df = df[df['Příjmení'].apply(remove_diacritics).str.lower().str.startswith(value, na=False)].drop_duplicates().head(5)
        return list(zip(slice_df['Příjmení'],
                        slice_df['Jméno'],
                        slice_df['Login'],
                        slice_df['Typ cert.'],
                        slice_df['Platnost do'],))

    return None
def excel_path_load(config,path,safe_write_config):
    if c.EXCEL_SECTION not in config:
        raise ValueError("Chybí sekce EXCEL")
    config.set(c.EXCEL_SECTION, c.EXCEL_PATH, path)
    safe_write_config(config, c.CONFIG_PATH)
def renew_excel_path():
    pass
