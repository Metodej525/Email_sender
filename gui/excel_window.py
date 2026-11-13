import pandas as pd
import constants as c
import configparser

from pathlib import Path
from collections.abc import Callable

from tkinter import Button, Label, Frame, Entry, ttk

from core.protocols import AppStateProtocol


class ExcelTab(Frame):
    def __init__(self, notebook: ttk.Notebook,
                 safe_write_config: Callable[[configparser.ConfigParser,str],None],
                 config: configparser.ConfigParser,
                 ExcelLoader,
                 excel_raw_load: Callable[[str | Path,str],pd.DataFrame],
                 SheetManager,
                 excel_path_load: Callable[[configparser.ConfigParser,str,
                                            Callable[[configparser.ConfigParser, str], None]
                                            ],None],
                 app_state: AppStateProtocol):
        # inicializace rodičovské třídy
        super().__init__(notebook)

        # funkce pro načítání excelu
        self.ExcelLoader = ExcelLoader

        self.SheetManager = SheetManager
        # dataframe s daty z excelu
        self.app_state = app_state

        # funkce pro bezpečný zápis configu
        self.safe_write_config = safe_write_config

        # konfigurace
        self.config = config

        #
        self.excel_path_load = excel_path_load

        #
        self.excel_raw_load= excel_raw_load

        # input pole pro zadání cesty k souboru
        self.path_entry = Entry(self)
        self.path_entry.grid(column=0, row=0, sticky="nw", padx=5, pady=5)

        # načtení aktuální cesty z configu
        excel_path = self.config.get(c.EXCEL_SECTION, c.EXCEL_PATH)

        # vložení cesty do inputu
        self.path_entry.insert(0, f'{excel_path}')

        # tlačítko pro reload excelu
        button_reload_excel = Button(
            self,
            text='reload excel file',
            command=self.reload_excel
        )
        button_reload_excel.grid(column=1, row=0, sticky="nw", padx=5, pady=5)

        self.sheet_bnt_list = []

        self.initial_excel_load()

    def initial_excel_load(self) -> None:
        try:

            # Získání dostupných listů a jejich počtu
            sheet_list, number_of_sheets = self.SheetManager(self.config).sheet_checker()

            # Načtení prvního listu a vytvoření tlačítek pro přepínání
            self.ExcelLoader(self.config,self.excel_raw_load,sheet_list[0],self.app_state).excel_load()
            self.sheet_button(number_of_sheets, sheet_list)
        except Exception as e:

            # Zobrazení chybového hlášení s automatickým odstraněním po 5 sekundách
            excel_error_label = Label(
                self,
                text=f'Chyba při načítání Excelu: {e}'
            )
            excel_error_label.grid(column=1, row=2, sticky="nw", padx=5, pady=5)
            self.after(5000, excel_error_label.destroy)

    def load_excel_sheet(self,
                         sheet: str,
                         ) -> None:
        try:

            # Načtení uživatelem vybraného listu
            self.ExcelLoader(self.config,self.excel_raw_load,sheet,self.app_state).excel_load()

        except Exception as e:

            # Ošetření chyby při načítání konkrétního listu
            excel_error_label = Label(
                self,
                text=f'Chyba při načítání Excelu: {e}'
            )
            excel_error_label.grid(column=1, row=2, sticky="nw", padx=5, pady=5)
            self.after(5000, excel_error_label.destroy)

    def sheet_button(self,
                     number_of_sheets: int,
                     sheet_list: list[str],
                     ) -> None:

        # Dynamické vytvoření tlačítka pro každý dostupný list
        for n,_ in enumerate(range(number_of_sheets)):
            sheet_btn = Button(self,
                               text=n + 1,
                               # Výchozí argument lambda uchovává správný list pro každé tlačítko
                               command=lambda sheet=sheet_list[n]: self.sheet_loader(sheet))
            sheet_btn.grid(column=0, row=n + 1, sticky="nw", padx=5, pady=5)
            self.sheet_bnt_list.append(sheet_btn)

    def sheet_loader(self,
                     selected_sheet: str
                     ) -> None:

        # Předání vybraného listu k načtení
        self.load_excel_sheet(selected_sheet)

    def reload_excel(self) -> None:

        # Aktualizace cesty k Excelu a obnovení seznamu dostupných listů
        path = self.path_entry.get()
        self.excel_path_load(self.config,path,self.safe_write_config)

        # Odstranění původních tlačítek před vytvořením nových
        for widget in self.sheet_bnt_list:
            widget.destroy()
        self.sheet_bnt_list.clear()
        self.initial_excel_load()