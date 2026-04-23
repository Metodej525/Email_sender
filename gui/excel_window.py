from tkinter import Button, Label, Frame, Entry
import constants as c

class ExcelTab(Frame):
    def __init__(self, notebook, excel_path_load, safe_write_config, config, excel_load):
        # inicializace rodičovské třídy (Frame v Tkinteru)
        super().__init__(notebook)

        # funkce pro načítání excelu (předaná zvenku)
        self.excel_load = excel_load

        # dataframe s daty z excelu (zatím None)
        self.df = None

        # funkce pro změnu cesty k excelu
        self.excel_path_load = excel_path_load

        # funkce pro bezpečný zápis configu
        self.safe_write_config = safe_write_config

        # konfigurace (pravděpodobně configparser)
        self.config = config

        # tlačítko pro přepsání cesty k excel souboru
        renew_excel_path_button = Button(
            self,
            text='Přepsání cesty k souboru',
            command=self.renew_excel_path
        )
        renew_excel_path_button.grid(column=1, row=0, sticky="nw", padx=5, pady=5)

        # input pole pro zadání cesty k souboru
        self.path_entry = Entry(self)
        self.path_entry.grid(column=0, row=0, sticky="nw", padx=5, pady=5)

        # načtení aktuální cesty z configu
        excel_path = self.config.get("EXCEL", 'path')

        # vložení cesty do inputu
        self.path_entry.insert(0, f'{excel_path}')

        # tlačítko pro reload excelu
        button_reload_excel = Button(
            self,
            text='reload excel file',
            command=self.reload_excel
        )
        button_reload_excel.grid(column=0, row=1, sticky="nw", padx=5, pady=5)

        # při vytvoření tabu se rovnou pokusí načíst excel
        self.load_excel()

        self.load_excel()

    def load_excel(self):
        try:
            self.df = self.excel_load(self.config.get(c.EXCEL_SECTION,c.EXCEL_PATH))
        except Exception as e:
            excel_error_label = Label(
                self,
                text=f'Chyba při načítání Excelu: {e}'
            )
            excel_error_label.grid(column=1, row=2, sticky="nw", padx=5, pady=5)
            self.after(5000, excel_error_label.destroy)

    def renew_excel_path(self):
        # získání cesty z inputu
        path = self.path_entry.get()

        # zavolání funkce pro změnu cesty v configu
        self.excel_path_load(self.config, path, self.safe_write_config)

    def reload_excel(self):
        # znovunačtení excelu
        self.load_excel()