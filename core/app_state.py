import pandas as pd


class AppState:
    #nastavení instance dataframu sdílené napříč aplikací
    def __init__(self) -> None:
        self.df = None

    def set_df(self, df) -> None:
        self.df = df

    def get_df(self) -> pd.DataFrame:
        return self.df