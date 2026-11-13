from typing import Protocol
import pandas as pd

class AppStateProtocol(Protocol):

    def set_df(self, df: pd.DataFrame) -> None:
        ...

    def get_df(self) -> pd.DataFrame | None:
        ...

class EmailDataProtocol(Protocol):
    exp_date: str
    exp_time: str
    email_body: str
    email: str
    importance: int