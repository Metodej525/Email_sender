###Technologie
#pyinstaller pro vytvoreni .exe
#smtplib email.mime.text na poslani a vytvoreni sablony e-mailu
#logování

import configparser
import os
import sys
from tkinter import *
from tkinter import ttk

from gui.email_preview_window import EmailPreviewTab
from gui.email_window import EmailTab
from gui.excel_window import ExcelTab
from gui.signature_window import SignatureTab

from Service.email_service import load_email_details, selected_value_manager, specific_email_preview, html_converter, email_sender
from Service.excel_service import excel_path_load, excel_search, excel_load
from Service.signature_service import save_signature, load_signature_data

from utils import safe_write_config
import constants as c

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

config_path = os.path.join(BASE_DIR, "config.ini")

#config.ini nacteni
config = configparser.ConfigParser()
config.read(filenames=c.CONFIG_PATH, encoding=c.CONFIG_ENCODING)

root = Tk()
notebook = ttk.Notebook(root)
notebook.pack(expand=True,fill='both')
root.title(c.ROOT_TITLE)
root.option_add("*Font", ("Arial", 12))

#signature_tab = SignatureTab(notebook,config,save_signature,safe_write_config,load_signature_data)
email_preview_tab = EmailPreviewTab(notebook,load_email_details,html_converter,config )
excel_tab = ExcelTab(notebook,excel_path_load,safe_write_config,config,excel_load)
email_tab = EmailTab(notebook,root,excel_search,config,excel_tab.df,selected_value_manager,html_converter, email_sender,specific_email_preview)


notebook.add(email_tab, text="Email")
notebook.add(email_preview_tab,text='Náhled emialu')
#notebook.add(signature_tab, text="Signature")
notebook.add(excel_tab, text="Excel")

TAB_FIELDS = {
    email_tab: '700x350',
    email_preview_tab: '1200x600',
    #signature_tab: '300x200',
    excel_tab: '600x300'
}
def resize_tab(event):
    tab_id = event.widget.select()
    tab = event.widget.nametowidget(tab_id)

    if tab in TAB_FIELDS:
        root.geometry(TAB_FIELDS[tab])

notebook.bind("<<NotebookTabChanged>>", resize_tab)
root.geometry("500x150")
root.mainloop()








