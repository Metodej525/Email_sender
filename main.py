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
from gui.signature_window import SignatureTab
from gui.email_window import EmailTab
from gui.excel_window import ExcelTab
from gui.email_preview_window import EmailPreviewTab
from utils import safe_write_config
from logic.signature_manager import save_signature,load_signature_data
from logic.email_manager import send_email, load_email_details
from logic.excel_manager import excel_path_load, excel_search

#config.ini nacteni
config= configparser.ConfigParser()
config.read('config.ini', encoding="cp1250")

#nacteni zpravy pro budouci upravy
message = config.get(section="EMAIL",option="body")
#cesta k excel souboru
excel_path=config.get(section="EXCEL",option='path')

root = Tk()
notebook = ttk.Notebook(root)
notebook.pack(expand=True,fill='both')
root.title(":)")

email_tab = EmailTab(notebook,root)
signature_tab = SignatureTab(notebook,config,save_signature,safe_write_config,load_signature_data)
email_preview_tab = EmailPreviewTab(notebook,load_email_details,config)
excel_tab = ExcelTab(notebook,excel_path,excel_path_load,safe_write_config,config)


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








