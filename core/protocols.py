from __future__ import annotations

import configparser
import tkinter as tk
import pandas as pd

from collections.abc import Callable
from pathlib import Path
from typing import Protocol

# ---------------------------------------------------------------------------
# Application state
# ---------------------------------------------------------------------------

class AppStateProtocol(Protocol):
    """Definuje rozhraní pro přístup ke sdílenému stavu aplikace a jeho aktualizaci."""

    def set_df(self, df: pd.DataFrame) -> None: ...
    """Uloží aktuální DataFrame do stavu aplikace."""

    def get_df(self) -> pd.DataFrame | None: ...
    """Vrátí aktuálně uložený DataFrame, pokud je k dispozici."""

    def set_file_path(self, file_path_key: str, file_path_value: str) -> None: ...
    """Nastaví cestu k aktuálnímu excel souboru v AppState"""

    def get_file_path(self) -> tuple[str,str]: ...
    """Vrátí cestu k aktuálně načteném souboru Excel"""
# ---------------------------------------------------------------------------
# Datový model e-mailu
# ---------------------------------------------------------------------------

class EmailDataProtocol(Protocol):
    """Definuje datovou strukturu reprezentující jednu e-mailovou položku."""

    exp_date: str
    exp_time: str
    email_body: str
    email: str
    importance: int

# ---------------------------------------------------------------------------
# Načítání Excel souborů
# ---------------------------------------------------------------------------

class ExcelLoaderFactory(Protocol):
    """Definuje rozhraní továrny pro vytváření instancí načítače Excel souborů."""

    def __call__(
        self, config: configparser.ConfigParser,
        excel_raw_load: Callable[[str | Path, str], pd.DataFrame],
        app_state: AppStateProtocol,
    ) -> ExcelLoaderProtocol: ...
    """Vytvoří načítač Excel souborů s požadovanými závislostmi."""

class ExcelLoaderProtocol(Protocol):
    """Definuje rozhraní pro načítání dat z Excel souborů do aplikace."""

    def excel_load(self, path: str, sheet: str) -> None: ...
    """Načte a zpracuje data z vybraného listu Excel souboru."""

    def initial_excel_load(self,
                           first_path: str,
                           sheet_list: list[str]
                           ) -> None: ...
    """Načte první list Excelu při spuštění aplikace"""

# ---------------------------------------------------------------------------
# Správa listů v Excel souboru
# ---------------------------------------------------------------------------

class SheetManagerFactory(Protocol):
    """Definuje rozhraní továrny pro vytváření správců Excel listů."""

    def __call__(
        self, path: str,
            config: configparser.ConfigParser
    )-> SheetManagerProtocol: ...
    """Vytvoří správce Excel listů na základě konfigurace aplikace."""

class SheetManagerProtocol(Protocol):
    """Definuje rozhraní pro kontrolu a získávání informací o Excel listech."""

    def sheet_checker(self) -> tuple[list[str],int]: ...
    """Ověří dostupné listy a vrátí jejich názvy spolu s indexem vybraného listu."""

# ---------------------------------------------------------------------------
# Odesílání e-mailů
# ---------------------------------------------------------------------------

class EmailSendManagerFactory(Protocol):
    """Definuje rozhraní továrny pro vytváření správců odesílání e-mailů."""

    def __call__(self,config: configparser.ConfigParser,
                 email_data: list[EmailDataProtocol],
                 email_details: Callable[[configparser.ConfigParser,str,str],None],
                 ) -> EmailSendManagerProtocol: ...
    """Vytvoří správce odesílání e-mailů s požadovanými závislostmi."""

class EmailSendManagerProtocol(Protocol):
    """Definuje rozhraní pro kontrolu a odesílání e-mailů."""

    def email_non_state_checker(self) -> None: ...
    """Zkontroluje data e-mailů před jejich odesláním."""

    def email_sender(self) -> None: ...
    """Zajišťuje proces odesílání e-mailů."""

# ---------------------------------------------------------------------------
# Sestavování obsahu e-mailů
# ---------------------------------------------------------------------------

class EmailConstructorFactory(Protocol):
    """Definuje rozhraní továrny pro vytváření objektů sestavujících e-maily."""
    def __call__(self,config: configparser.ConfigParser,
                 data: list[EmailDataProtocol] | None | EmailDataProtocol,
                 importance_toggle: Callable[[str,int],str]
                 ) -> EmailConstructorProtocol: ...
    """Vytvoří objekt pro sestavování e-mailů na základě předaných dat a konfigurace."""

class EmailConstructorProtocol(Protocol):
    """Definuje rozhraní pro sestavování obsahu e-mailových zpráv."""

    def email_body_constructor(self, email_row: EmailDataProtocol) -> str: ...
    """Sestaví tělo e-mailu na základě dat konkrétní e-mailové položky."""

    def set_email_body(self) -> None: ...
    """Nastaví nebo aktualizuje obsah e-mailu podle dostupných dat."""


# ---------------------------------------------------------------------------
# Uživatelská komponenta jednotlivého e-mailového řádku
# ---------------------------------------------------------------------------

class EmailRowFactory(Protocol):
    """Definuje rozhraní továrny pro vytváření jednotlivých e-mailových řádků."""
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
    """Vytvoří e-mailový řádek a předá mu potřebné závislosti."""

class EmailRowProtocol(Protocol):
    """Definuje rozhraní jednotlivého e-mailového řádku v uživatelském rozhraní."""

    entry_email: EntryProtocol | tk.Widget
    email: str | None

    def set_data(self) -> EmailDataProtocol: ...
    """Získá a vrátí aktuální data e-mailového řádku."""

    def safe_set_values(
        self,
        email: str,
        exp_date: str,
        exp_time: str,
    ) -> None: ...
    """Aktualizuje hodnoty řádku s ohledem na možné neplatné vstupy."""



    def destroy(self) -> None: ...
    """Odstraní e-mailový řádek a jeho přidružené prvky uživatelského rozhraní."""

# ---------------------------------------------------------------------------
# Nadřazená komponenta e-mailových řádků
# ---------------------------------------------------------------------------

class EmailRowParentProtocol(Protocol):
    """Definuje rozhraní nadřazené komponenty spravující e-mailové řádky."""

    dropdown: EmailDropDownProtocol | None

    def focus_dropdown(self, row: EmailRowProtocol) -> None: ...
    """Přesune fokus na rozbalovací nabídku příslušného e-mailového řádku."""

    def on_search_change(self, row: EmailRowProtocol) -> None: ...
    """Zpracuje změnu vyhledávacího vstupu v konkrétním e-mailovém řádku."""

    def on_select(self, event: tk.Event | None = None) -> None: ...
    """Zpracuje událost výběru položky v uživatelském rozhraní."""

# ---------------------------------------------------------------------------
# Seznam dostupných e-mailových adres
# ---------------------------------------------------------------------------

class EmailListboxProtocol(Protocol):
    """Definuje požadované rozhraní komponenty Listbox z knihovny Tkinter."""

    def focus_set(self) -> None: ...
    """Přiřadí komponentě Listbox klávesnicový fokus."""

    def selection_clear(self,first: int | str,
                        last: int | str) -> None: ...
    """Zruší aktuální výběr v zadaném rozsahu položek."""

    def selection_set(self,first: int | str,
                      last = None) -> None: ...
    """Vybere konkrétní položku nebo rozsah položek v seznamu."""

    def activate(self,index: int | str) -> None: ...
    """Nastaví zadanou položku jako aktivní."""

# ---------------------------------------------------------------------------
# Rozbalovací nabídka e-mailových adres
# ---------------------------------------------------------------------------

class EmailDropDownProtocol(Protocol):
    """Definuje rozhraní rozbalovací nabídky s návrhy e-mailových adres."""

    listbox: EmailListboxProtocol

    def destroy(self) -> None: ...
    """Odstraní rozbalovací nabídku a uvolní související prostředky uživatelského rozhraní."""

# ---------------------------------------------------------------------------
# Textový vstup
# ---------------------------------------------------------------------------

class EntryProtocol(Protocol):
    """Definuje minimální rozhraní požadované od textového vstupního pole."""

    def get(self) -> str: ...
    """Vrátí aktuální textovou hodnotu vstupního pole."""
