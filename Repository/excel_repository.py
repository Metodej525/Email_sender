import pandas as pd

def excel_raw_load(filepath):
    df = pd.read_excel(filepath)
    return df
