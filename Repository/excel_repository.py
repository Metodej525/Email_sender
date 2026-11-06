import pandas as pd

def excel_raw_load(filepath,sheet):
    #načte excel soubor s daty
    df = pd.read_excel(filepath,sheet_name=sheet)
    return df

