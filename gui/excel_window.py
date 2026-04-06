from tkinter import Button, Label, Frame, Entry

class ExcelTab(Frame):
    def __init__(self,notebook,excel_path_load,safe_write_config, config, df, excel_load):
        super().__init__(notebook)
        # self.reset_email_tab = reset_tab

        self.excel_load = excel_load
        self.df = df
        self.excel_path_load = excel_path_load
        self.safe_write_config = safe_write_config
        self.config = config
        #cesta k entry s insertem cesty k souboru .xlx + button na nastaveni cesty
        renew_excel_path_button = Button(self,text='Přepsání cesty k souboru',command=self.renew_excel_path)
        renew_excel_path_button.grid(column=1,row=0,sticky="nw",padx=5, pady=5)
        self.path_entry = Entry(self)
        self.path_entry.grid(column=0, row=0,sticky="nw",padx=5, pady=5)

        excel_path = self.config.get("EXCEL",'path')
        self.path_entry.insert(0,f'{excel_path}')
        button_reload_excel = Button(self,
                                         text='reload excel file',
                                         command=self.reload_excel)
        button_reload_excel.grid(column=0, row=1,sticky="nw",padx=5, pady=5)

        self.load_excel()
    def load_excel(self):
        self.excel_load(self.config)
        if self.df is None:
            self.df, self.excel_load_error = self.excel_load(self.config)
            excel_error_label = Label(self, text=f'Chyba při načítání Excelu: {self.excel_load_error}')
            excel_error_label.grid(column=1, row=2,sticky="nw",padx=5, pady=5)
            self.after(5000, excel_error_label.destroy)

        excel_error_label = Label(self, text=f'Chyba při načítání Excelu: {self.excel_load_error}')
        excel_error_label.grid(column=1, row=2,sticky="nw",padx=5, pady=5)
        self.after(5000, excel_error_label.destroy)
        #
        # try:
        #     excel_success_label = Label(self, text=f'Excel soubor úspěšně načten')
        #     excel_success_label.grid(column=1, row=2,sticky="nw",padx=5, pady=5)
        #     self.after(5000, excel_success_label.destroy)
        #     return True, self.df
        # except Exception as e:
        #     excel_error_label = Label(self, text=f'Chyba při načítání Excelu: {e}')
        #     excel_error_label.grid(column=1, row=2,sticky="nw",padx=5, pady=5)
        #     self.after(5000, excel_error_label.destroy)
        #     return False, None
    def renew_excel_path(self):
        path = self.path_entry.get()
        self.excel_path_load(self.config,path,self.safe_write_config)
    def reload_excel(self):
        # self.reset_email_tab()
        self.load_excel()