class AppState:
    #nastavení instance dataframu sdílené napříč appkou
    def __init__(self):
        self.df = None

    def set_df(self, df):
        self.df = df

    def get_df(self):
        return self.df