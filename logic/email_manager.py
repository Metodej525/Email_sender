from tkinter import *
from functools import partial



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

buttons = []
email_entries = []
date_entries = []
def add_email_receiver(email_tab):
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
