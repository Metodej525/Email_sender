###Technologie
#pyinstaller pro vytvoreni .exe
#smtplib email.mime.text na poslani a vytvoreni sablony e-mailu
#keyring pro Windows Credential Manager na ulozeni hesla
#logování
#realtime vyhledavani v .csv souboru a nacteni uzivatele
#moznost vybrat vice emailu
#potvrzeni odeslani mailu
import configparser
from tkinter import *
from tkinter import ttk

from gui.email_preview_window import EmailPreviewTab
from gui.email_window import EmailTab
from gui.excel_window import ExcelTab
from gui.signature_window import SignatureTab
from Service.email_service import load_email_details, selected_value_manager
from Service.excel_service import excel_path_load, excel_search, excel_load
from Service.signature_service import save_signature, load_signature_data
from utils import safe_write_config
import constants as c

#config.ini nacteni
config = configparser.ConfigParser()
config.read(filenames=c.CONFIG_PATH, encoding=c.CONFIG_ENCODING)

#nacteni zpravy pro budouci upravy
message = config.get(section=c.EMAIL_SECTION,option=c.EMAIL_BODY)



root = Tk()
notebook = ttk.Notebook(root)
notebook.pack(expand=True,fill='both')
root.title(c.ROOT_TITLE)

signature_tab = SignatureTab(notebook,config,save_signature,safe_write_config,load_signature_data)
email_preview_tab = EmailPreviewTab(notebook,load_email_details,config )
excel_tab = ExcelTab(notebook,excel_path_load,safe_write_config,config,excel_load)
email_tab = EmailTab(notebook,root,excel_search,config,excel_tab.df,selected_value_manager)


notebook.add(email_tab, text="Email")
notebook.add(email_preview_tab,text='Náhled emialu')
notebook.add(signature_tab, text="Signature")
notebook.add(excel_tab, text="Excel")

def resize_tab(event):
    tab_id = event.widget.select()
    tab = event.widget.nametowidget(tab_id)

    if tab == email_tab:
        root.geometry("500x300")
    elif tab == email_preview_tab:
        root.geometry("800x600")
    elif tab == signature_tab:
        root.geometry('300x200')
    elif tab == excel_tab:
        root.geometry("600x200")

notebook.bind("<<NotebookTabChanged>>", resize_tab)
root.geometry("500x150")
root.mainloop()








