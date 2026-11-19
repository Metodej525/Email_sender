from __future__ import annotations
import configparser
import tkinter as tk
import pandas as pd
from collections.abc import Callable
from pathlib import Path
from typing import Protocol


class AppStateProtocol(Protocol):

    def set_df(self, df: pd.DataFrame) -> None: ...

    def get_df(self) -> pd.DataFrame | None: ...

class EmailDataProtocol(Protocol):
    exp_date: str
    exp_time: str
    email_body: str
    email: str
    importance: int

class ExcelLoaderFactory(Protocol):
    def __call__(
        self, config: configparser.ConfigParser,
        excel_raw_load: Callable[[str | Path, str], pd.DataFrame],
        selected_sheet: str,
        app_state: AppStateProtocol,
    ) -> ExcelLoaderProtocol: ...

class ExcelLoaderProtocol(Protocol):

    def excel_load(self) -> None: ...

class SheetManagerFactory(Protocol):
    def __call__(
        self, config: configparser.ConfigParser
    )-> SheetManagerProtocol: ...

class SheetManagerProtocol(Protocol):

    def sheet_checker(self) -> tuple[list[str],int]: ...

class EmailSendManagerFactory(Protocol):
    def __call__(self,config: configparser.ConfigParser,
                 email_data: list[EmailDataProtocol],
                 email_details: Callable[[configparser.ConfigParser,str,str],None],
                 ) -> EmailSendManagerProtocol: ...

class EmailSendManagerProtocol(Protocol):
    def email_non_state_checker(self) -> None: ...

    def email_sender(self) -> None: ...

class EmailConstructorFactory(Protocol):
    def __call__(self,config: configparser.ConfigParser,
                 data: list[EmailDataProtocol] | None | EmailDataProtocol,
                 importance_toggle: Callable[[str,int],str]
                 ) -> EmailConstructorProtokol: ...

class EmailConstructorProtokol(Protocol):

    def email_body_constructor(self, email_row: EmailDataProtocol) -> str: ...

    def set_email_body(self) -> None: ...

class EmailRowFactory(Protocol):
    def __call__(
        self,
        parent: EmailRowParentProtocol,
        config: configparser.ConfigParser,
        remove_callback: Callable[[EmailRowProtocol], None],
        EmailConstructor: EmailConstructorFactory,
        html_converter: Callable[[str], str],
        root: tk.Tk,
        importance_toggle: Callable[[str, int], str],
    ) -> EmailRowProtocol: ...

class EmailRowProtocol(Protocol):
    entry_email: EntryProtocol | tk.Widget
    email: str | None

    def set_data(self) -> EmailDataProtocol: ...

    def safe_set_values(
        self,
        email: str,
        exp_date: str,
        exp_time: str,
    ) -> None: ...



    def destroy(self) -> None: ...

class EmailRowParentProtocol(Protocol):
    dropdown: EmailDropDownProtocol | None

    def focus_dropdown(self, row: EmailRowProtocol) -> None: ...

    def on_search_change(self, row: EmailRowProtocol) -> None: ...

    def on_select(self, event: tk.Event | None = None) -> None: ...


class EmailListboxProtocol(Protocol):
    def focus_set(self) -> None: ...

    def selection_clear(self,first: int | str,
                        last: int | str) -> None: ...

    def selection_set(self,first: int | str,
                      last = None) -> None: ...

    def activate(self,index: int | str) -> None: ...

class EmailDropDownProtocol(Protocol):
    listbox: EmailListboxProtocol

    def destroy(self) -> None: ...

class EntryProtocol(Protocol):
    def get(self) -> str: ...
