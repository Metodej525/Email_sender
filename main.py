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
from logic.email_manager import add_email_receiver
from utils import safe_write_config
from logic.signature_manager import save_signature
#config.ini nacteni
config= configparser.ConfigParser()
config.read('config.ini', encoding="cp1250")

#nacteni zpravy pro budouci upravy
message = config.get("EMAIL","body")


root = Tk()
notebook = ttk.Notebook(root)
notebook.pack(expand=True,fill='both')

email_tab = EmailTab(notebook,add_email_receiver)
signature_tab = SignatureTab(notebook,config,save_signature,safe_write_config)

root.mainloop()








