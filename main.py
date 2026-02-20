import configparser
from tkinter import *
from tkinter import ttk
from scripts import safe_write_config
from functools import partial

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
def send_email(date_list,email_list):
    #vytvori potvrzovaci label
    # temp_label = Label(email_tab, text='mail odeslán')
    # temp_label.grid(column=1,row=3, columnspan=2)
    #po 2 sekundách label skryje, pro kazdy label bezi samostatny timeout jestli nekdo bude klikat jak jeblej tak se to rozbije
    # root.after(2000, temp_label.destroy)
    date_list.pop(0)
    email_list.pop(0)
    for x in date_list:
        x.destroy()
    for y in email_list:
        y.destroy()
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

    safe_write_config(config,'config.ini')


    #ulozi podpis do .ini file
    # vytvori potvrzovaci label
    temp_label = Label(signature_tab, text='podpis uložen')
    temp_label.grid(column=0, row=4, columnspan=2)
    # po 2 sekundách label skryje, pro kazdy label bezi samostatny timeout jestli nekdo bude klikat jak jeblej tak se to rozbije
    root.after(2000, temp_label.destroy)

buttons = []
email_entries = []
date_entries = []
def add_email_receiver():
    entry_email = Entry(email_tab)
    entry_email.grid(column=0, row=len(email_entries))

    entry_date = Entry(email_tab)
    entry_date.grid(column=1,row= len(email_entries))

    date_entries.append(entry_date)
    email_entries.append(entry_email)

    button =Button(email_tab,
            text='odeslat mail',
            command=partial(send_email, email_entries, date_entries))
    button.grid(column=1,row=len(email_entries)+1)

    buttons.append(button)
    if len(buttons) > 1:
        old_button = buttons.pop(0)
        old_button.destroy()
#nastavení záložek
notebook = ttk.Notebook(root)
notebook.pack(expand=True,fill='both')


## první záložka
email_tab = Frame(notebook)
notebook.add(email_tab, text='Email')
Button(email_tab, text='přidej email', command=add_email_receiver).grid(column=2,row=0)
#label s obsahem mailu
# Label(email_tab, text=message).grid(column=0,row=2)






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
Label(signature_tab, text='Pracovní pozice').grid(column=0,row=2)
position_entry = Entry(signature_tab)
position_entry.grid(column=1,row=2)
#label + entry na organizační členění
Label(signature_tab, text='Org. členění').grid(column=0,row=3)
department_entry = Entry(signature_tab)
department_entry.grid(column=1,row=3)
#login
Label(signature_tab, text='Login').grid(column=0,row=4)
login_entry = Entry(signature_tab)
login_entry.grid(column=1,row=4)
#button na uložení podpisu
Button(signature_tab, text='uložit podpis',command=save_signature).grid(column=1,row=5)
notebook.add(signature_tab, text='Podpis')

root.mainloop()


