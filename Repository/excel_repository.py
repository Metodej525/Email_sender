from pathlib import Path

import pandas as pd

def excel_raw_load(filepath: str | Path,
                   sheet: str
                   ) -> pd.DataFrame:
    #načte excel soubor s daty
    df = pd.read_excel(filepath,sheet_name=sheet)
    return df

