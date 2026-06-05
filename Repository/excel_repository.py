import pandas as pd

def excel_raw_load(filepath,sheet):
    df = pd.read_excel(filepath,sheet_name=sheet)
    return df

