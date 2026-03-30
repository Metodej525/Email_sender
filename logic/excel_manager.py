import pandas as pd
import unicodedata


def excel_load(config):
    path = config.get("EXCEL", "path")
    try:
        df = pd.read_excel(path)
        return df
    except Exception as e:
        raise RuntimeError(f"Chyba při načítání {path}") from e
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
def excel_path_load(config,path,write_config):
    if "EXCEL" not in config:
        raise ValueError("Chybí sekce EXCEL")
    config.set("EXCEL", 'path', path)
    write_config(config, "config.ini")
