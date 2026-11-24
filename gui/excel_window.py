import pandas as pd
import configparser

from pathlib import Path
from collections.abc import Callable
from tkinter import Button, Label, Frame, Entry, ttk

from core.protocols import AppStateProtocol, ExcelLoaderFactory, SheetManagerFactory


class ExcelTab(Frame):
    def __init__(self, notebook: ttk.Notebook,
                 safe_write_config: Callable[[configparser.ConfigParser,str],None],
                 config: configparser.ConfigParser,
                 ExcelLoader: ExcelLoaderFactory,
                 excel_raw_load: Callable[[str | Path,str],pd.DataFrame],
                 SheetManager: SheetManagerFactory,
                 excel_path_load: Callable[[configparser.ConfigParser,str, str, list[str],
                                            Callable[[configparser.ConfigParser, str], None]],
                                            Callable[[str], None],AppStateProtocol,None],
                 get_excel_path_status,
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
        self.get_excel_path_status = get_excel_path_status
        #
        self.excel_path_load = excel_path_load

        #
        self.excel_raw_load= excel_raw_load

        self.sheet_bnt_list = []

        # Nastavení slovníku s cestami k více Excel souborům
        self.path_dict = self.get_excel_path_status(self.config)

        self.load_initial_layout()

        self.initial_excel_load()

    def initial_excel_load(self) -> None:
        key_list = list(self.path_dict.keys())

        try:
            # Získání dostupných listů a jejich počtu
            sheet_list, number_of_sheets = self.SheetManager(key_list[0],self.config).sheet_checker()

            # První položka v slovniku self.path_dict
            first_path = next(iter(self.path_dict.values()))

            # Načtení prvního listu a vytvoření tlačítek pro přepínání
            self.ExcelLoader(self.config,self.excel_raw_load,self.app_state).initial_excel_load(first_path,sheet_list)
            self.sheet_button(number_of_sheets, sheet_list)

        except Exception as e:
            # Zobrazení chybového hlášení s automatickým odstraněním po 5 sekundách

            excel_error_label = Label(
                self,
                text=f'Chyba při načítání Excelu: {e}'
            )
            excel_error_label.grid(column=1, row=2, sticky="nw", padx=5, pady=5)
            self.after(5000, excel_error_label.destroy)

    def load_initial_layout(self):
        # Načte layout okna podle toho kolik je definovaných cest v configu
        # Nastaví path_key a path_value v AppState

        set_path_key, set_path_value = next(iter(self.path_dict.items()))
        self.app_state.set_file_path(set_path_key,set_path_value)
        sheet_list, number_of_sheets = self.SheetManager(set_path_key, self.config).sheet_checker()

        for n, (key, path_value) in enumerate(self.path_dict.items()):

            path_entry = Entry(self)
            path_entry.grid(column=0, row=n, sticky="w", padx=5, pady=5)
            path_entry.insert(0, f'{path_value}')

            button_excel = Button(self,
                text='Load Excel',
                                  command=lambda key=key, path_value=path_value: self.reload_excel(
                                      sheet=sheet_list[0],
                                      path_key=key,
                                      path_value=path_value))
            button_excel.grid(column=1, row=n, sticky="nw", padx=5, pady=5)

    def load_excel_sheet(self,
                         sheet: str,
                         ) -> None:
        try:

            # Načtení uživatelem vybraného listu
            path_key, path_value = self.app_state.get_file_path()
            self.ExcelLoader(self.config,self.excel_raw_load,self.app_state).excel_load(path_value, sheet)

        except Exception as e:

            # Ošetření chyby při načítání konkrétního listu
            excel_error_label = Label(
                self,
                text=f'Chyba při načítání Excelu: {e}'
            )
            excel_error_label.grid(column=1, row=2, sticky="w", padx=5, pady=5)
            self.after(5000, excel_error_label.destroy)

    def sheet_button(self,
                     number_of_sheets: int,
                     sheet_list: list[str],
                     ) -> None:
        sheet_label = Label(self,text='Listy', padx=25)
        sheet_label.grid(column=2,row=0, sticky="e")
        # Dynamické vytvoření tlačítka pro každý dostupný list
        for n,_ in enumerate(range(number_of_sheets)):
            sheet_btn = Button(self,
                               text= n + 1,
                               # Výchozí argument lambda uchovává správný list pro každé tlačítko
                               command=lambda sheet=sheet_list[n]: self.sheet_loader(sheet))
            sheet_btn.grid(column=n + 3, row= 0, padx=5, pady=5)
            self.sheet_bnt_list.append(sheet_btn)

    def sheet_loader(self,
                     selected_sheet: str
                     ) -> None:

        # Předání vybraného listu k načtení
        self.load_excel_sheet(selected_sheet)

    def reload_excel(self,
                     path_key: str,
                     path_value: str,
                     sheet: str) -> None:

        # Aktualizace cesty k Excelu a obnovení seznamu dostupných listů
        self.excel_path_load(self.config,
                             path_key,
                             path_value,
                             sheet,
                             self.safe_write_config,
                             self.ExcelLoader(self.config,self.excel_raw_load,self.app_state).excel_load,
                             self.app_state)

        # Odstranění původních tlačítek před vytvořením nových
        for widget in self.sheet_bnt_list:
            widget.destroy()
        self.sheet_bnt_list.clear()

        # Znovu načtení widgetů listů excelu
        sheet_list, number_of_sheets = self.SheetManager(self.app_state.get_file_path()[0],self.config).sheet_checker()
        self.sheet_button(number_of_sheets, sheet_list)