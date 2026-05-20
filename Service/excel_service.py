import constants as c
from Repository.excel_repository import excel_raw_load
from utils import remove_diacritics

def excel_load(config):
    filepath = config.get(c.EXCEL_SECTION,c.EXCEL_PATH)
    try:
        df = excel_raw_load(filepath)
        return initial_filter(df)
    except Exception as e:
        print(e)
        raise

def initial_filter(df):
    """vyfiltruje jen certifikáty typu Q-TW-CZ"""
    df = df[
        df['Typ cert.']
        .fillna('')
        .str.strip()
        .eq('Q-TW-CZ')
    ]
    return df

def excel_search(value,df):
    # if df is not None:
    #     slice_df = df[df['Příjmení'].apply(remove_diacritics).str.lower().str.startswith(value, na=False)].drop_duplicates().head(5)
    #     if slice_df.empty:
    #         slice_df = df[df['Login'].apply(remove_diacritics).str.lower().str.startswith(value,
    #                                                                                          na=False)].drop_duplicates().head(
    #             5)
    #         if slice_df.empty:
    #             slice_df = df[df['Jméno'].apply(remove_diacritics).str.lower().str.startswith(value,
    #                                                                                              na=False)].drop_duplicates().head(
    #                 5)
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
        return list(zip(slice_df['Příjmení'],
                        slice_df['Jméno'],
                        slice_df['Login'],
                        slice_df['Typ cert.'],
                        slice_df['Platnost do'],))
    return []

def excel_path_load(config,path,safe_write_config):
    if c.EXCEL_SECTION not in config:
        raise ValueError("Chybí sekce EXCEL")
    config.set(c.EXCEL_SECTION, c.EXCEL_PATH, path)
    safe_write_config(config, c.CONFIG_PATH)


