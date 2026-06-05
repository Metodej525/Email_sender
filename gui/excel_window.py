from tkinter import Button, Label, Frame, Entry
import constants as c

class ExcelTab(Frame):
    def __init__(self, notebook,safe_write_config, config, ExcelLoader, excel_raw_load):
        # inicializace rodičovské třídy (Frame v Tkinteru)
        super().__init__(notebook)

        # funkce pro načítání excelu (předaná zvenku)
        self.ExcelLoader = ExcelLoader

        # dataframe s daty z excelu (zatím None)
        self.df = None

        # funkce pro bezpečný zápis configu
        self.safe_write_config = safe_write_config

        # konfigurace (pravděpodobně configparser)
        self.config = config

        self.excel_raw_load= excel_raw_load

        # # tlačítko pro přepsání cesty k excel souboru
        # renew_excel_path_button = Button(
        #     self,
        #     text='Přepsání cesty k souboru',
        #     command=self.renew_excel_path
        # )
        # renew_excel_path_button.grid(column=1, row=0, sticky="nw", padx=5, pady=5)

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

        self.load_excel()

    def load_excel(self):
        try:
            excel_loader = self.ExcelLoader(self.config,self.excel_raw_load)
            self.df = excel_loader.excel_load
            number_of_sheets = excel_loader.number_of_sheets
            self.create_sheet_btns(number_of_sheets)
        except Exception as e:
            excel_error_label = Label(
                self,
                text=f'Chyba při načítání Excelu: {e}'
            )
            excel_error_label.grid(column=1, row=2, sticky="nw", padx=5, pady=5)
            self.after(5000, excel_error_label.destroy)

    def create_sheet_btns(self,number_of_sheets):
        if number_of_sheets != 1:
            for _ in number_of_sheets:
                list_index = 0
                text_value = 1
                sheet = Button(
                    self,
                    text=f"{text_value}",
                    command= lambda: self.sheet_input(list_index)
                )
                sheet.grid(column=text_value-1, row=0, sticky="nw", padx=5, pady=5)
                list_index += 1
                text_value += 1
    def sheet_input(self, selected_value):
        return selected_value
    def reload_excel(self):
        # znovunačtení excelu
        self.load_excel()