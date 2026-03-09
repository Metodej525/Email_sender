from tkinter import Button, Label, Frame, Entry
import pandas as pd

class ExcelTab(Frame):
    def __init__(self,notebook,excel_file_path, reset_tab,excel_path_save,write_config, config):
        super().__init__(notebook)
        self.reset_email_tab = reset_tab
        self.excel_file_path = excel_file_path
        self.excel_path_save = excel_path_save
        self.write_config = write_config
        self.config = config
        #cesta k entry s insertem cesty k souboru .xlx + button na nastaveni cesty
        renew_excel_path_button = Button(self,text='Přepsání cesty k souboru',command=self.renew_excel_path)
        renew_excel_path_button.grid(column=1,row=0)
        self.path_entry = Entry(self)
        self.path_entry.grid(column=0, row=0)
        self.path_entry.insert(0,f'{self.excel_file_path}')
        button_reload_excel = Button(self,
                                         text='reload excel file',
                                         command=self.reload_excel)
        button_reload_excel.grid(column=0, row=1)

        self.load_excel()
    def load_excel(self):
        try:
            df = pd.read_excel(self.excel_file_path)
            excel_success_label = Label(self, text=f'Excel soubor úspěšně načten')
            excel_success_label.grid(column=0, row=2)
            self.after(5000, excel_success_label.destroy)
            return True,df
        except Exception as e:
            excel_error_label = Label(self, text=f'Chyba při načítání Excelu: {e}')
            excel_error_label.grid(column=0, row=2)
            self.after(5000, excel_error_label.destroy)
            return False, None
    def renew_excel_path(self):
        path = self.path_entry.get()
        self.excel_path_save(self.config,path,self.write_config)
    def reload_excel(self):
        self.reset_email_tab()
        self.load_excel()