import configparser
from tkinter import *
from tkinter import ttk

#config.ini nacteni
config= configparser.ConfigParser()
config.read('config.ini', encoding="cp1250")

#nacteni zpravy pro budouci upravy
message = config.get("EMAIL","body")

###Technologie
#pyinstaller pro vytvoreni .exe
#smtplib email.mime.text na poslani a vytvoreni sablony e-mailu
#keyring pro Windows Credential Manager na ulozeni hesla
#logování
#realtime vyhledavani v .csv souboru a nacteni uzivatele
#moznost vybrat vice emailu

#potvrzeni odeslani mailu
root = Tk()
def send_email():
    #vytvori potvrzovaci label
    temp_label = Label(email_tab, text='mail odeslán')
    temp_label.grid(column=1,row=3, columnspan=2)
    #po 2 sekundách label skryje, pro kazdy label bezi samostatny timeout jestli nekdo bude klikat jak jeblej tak se to rozbije
    root.after(2000, temp_label.destroy)
def save_signature():
    if "SIGNATURE" not in config:
        #logni error, zavri hlavni frame, vytvor novy s errorem
        pass
    #nastavi hodnoty (jmeno,telefon,oraganizacni cleneni) v ini souboru, otevre ho a ulozi, pokud je entry prazdne tak se neulozi
    fields = {
        "name": name_entry,
        "telephone": telephone_entry,
        "department": department_entry,
        "position": position_entry
    }

    for key, entry in fields.items():
        value = entry.get()
        if value != '':
            config.set('SIGNATURE', key, value)

    with open("config.ini", "w", encoding='cp1250') as f:
        config.write(f)

    #ulozi podpis do .ini file
    # vytvori potvrzovaci label
    temp_label = Label(signature_tab, text='podpis uložen')
    temp_label.grid(column=0, row=4, columnspan=2)
    # po 2 sekundách label skryje, pro kazdy label bezi samostatny timeout jestli nekdo bude klikat jak jeblej tak se to rozbije
    root.after(2000, temp_label.destroy)


#nastavení záložek
notebook = ttk.Notebook(root)
notebook.pack(expand=True,fill='both')


## první záložka
email_tab = Frame(notebook)
#email adresáta
email_entry = Entry(email_tab)
email_entry.grid(column=0,row=0)
#datum vypršení certifikátu + label jako vysvetlivka
Label(email_tab, text='datum vypršení certifikátu: ').grid(column=0,row=1)
date_entry = Entry(email_tab)
date_entry.grid(column=1,row=1)
#label dopsani domeny za mail
Label(email_tab, text='@ikem.cz').grid(column=1,row=0)
#label s obsahem mailu
Label(email_tab, text=message).grid(column=0,row=2)
#button odeslani mailu
Button(email_tab, text='odeslat mail', command=send_email).grid(column=1,row=3)
notebook.add(email_tab, text='Email')


## druhá záložka
signature_tab = Frame(notebook)
#label + entry na jméno a příjmení
Label(signature_tab, text='Jméno a přijmení: ').grid(column=0,row=0)
name_entry = Entry(signature_tab)
name_entry.grid(column=1,row=0)
#label + entry na tel. číslo
Label(signature_tab, text='Tel. číslo: ').grid(column=0,row=1)
telephone_entry = Entry(signature_tab)
telephone_entry.grid(column=1,row=1)
#label + entry na pozici pracovníka
position_entry = Entry(signature_tab)
position_entry.grid(column=1,row=2)
#label + entry na organizační členění
Label(signature_tab, text='Org. členění').grid(column=0,row=2)
department_entry = Entry(signature_tab)
department_entry.grid(column=1,row=3)
#button na uložení podpisu
Button(signature_tab, text='uložit podpis',command=save_signature).grid(column=1,row=4)
notebook.add(signature_tab, text='Podpis')

root.mainloop()


