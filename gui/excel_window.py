from tkinter import Button, Label, Frame
import pandas as pd

class ExcelTab(Frame):
    def __init__(self,notebook,excel_file_path):
        super().__init__(notebook)
        self.excel_file_path = excel_file_path

        button_reload_excel = Button(self,
                                         text='reload excel file',
                                         command=self.load_excel)
        button_reload_excel.grid(column=0, row=0)
        self.load_excel()
    def load_excel(self):
        try:
            pd.read_excel(self.excel_file_path)
            excel_success_label = Label(self, text=f'Excel soubor úspěšně načten')
            excel_success_label.grid(column=0, row=1)
            self.after(5000, excel_success_label.destroy)
        except FileNotFoundError:
            excel_error_label = Label(self, text=f'Excel nenalezen na {self.excel_file_path}')
            excel_error_label.grid(column=0, row=1)
            self.after(5000, excel_error_label.destroy)