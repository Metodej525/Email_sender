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
from utils import safe_write_config
from logic.signature_manager import save_signature,load_signature_data
from logic.email_manager import send_email
from gui.excel_window import ExcelTab

#config.ini nacteni
config= configparser.ConfigParser()
config.read('config.ini', encoding="cp1250")

#nacteni zpravy pro budouci upravy
message = config.get("EMAIL","body")
#cesta k excel souboru
excel_path='ahoj'


root = Tk()
notebook = ttk.Notebook(root)
notebook.pack(expand=True,fill='both')
root.title(":)")
root.geometry('400x300')
email_tab = EmailTab(notebook,send_email)
signature_tab = SignatureTab(notebook,config,save_signature,safe_write_config,load_signature_data)
excel_tab = ExcelTab(notebook,excel_path)

notebook.add(email_tab, text="Email")
notebook.add(signature_tab, text="Signature")
notebook.add(excel_tab, text="Excel")

root.mainloop()








