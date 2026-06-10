class AppState:
    def __init__(self):
        self.df = None

    def set_df(self, df):
        self.df = df

    def get_df(self):
        return self.df