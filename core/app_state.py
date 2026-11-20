import pandas as pd


class AppState:
    # Nastavení instance dataframu a cesty k Excelu sdílené napříč aplikací
    def __init__(self) -> None:
        self.df = None
        self.file_path_key = None
        self.file_path_value = None

    def set_df(self, df) -> None:
        self.df = df

    def set_file_path(self, file_path_key: str, file_path_value: str ) -> None:
        self.file_path_key = file_path_key
        self.file_path_value = file_path_value

    def get_file_path(self) -> tuple[str,str]:
        return self.file_path_key, self.file_path_value

    def get_df(self) -> tuple[pd.DataFrame, str]:
        return self.df