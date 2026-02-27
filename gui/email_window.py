from tkinter import Frame, Button, Entry, Label
from functools import partial



class EmailTab(Frame):
    def __init__(self,notebook, send_email):
        super().__init__(notebook)
        self.send_email = send_email

        Label(self, text='emailová schránka').grid(column=0,row=0)
        Label(self,text='datum ukončení certifikátu').grid(column=1,row=0)

        notebook.add(self, text='Email')
        Button(self, text='přidej email', command=partial(self.add_email_receiver)).grid(column=2,row=1)

        self.buttons = []
        self.email_entries = []
        self.date_entries = []
        self.default_widgets()



    def add_email_receiver(self):
        if len(self.email_entries) < 6:
            entry_email = Entry(self)
            entry_email.grid(column=0, row=len(self.email_entries) + 1)

            entry_date = Entry(self)
            entry_date.grid(column=1, row=len(self.email_entries)+ 1)
            button = Button(self,
                                 text='odeslat mail',
                                 command=partial(self.send_email, self.email_entries, self.date_entries))
            button.grid(column=1, row=len(self.email_entries) + 2)
            self.date_entries.append(entry_date)
            self.email_entries.append(entry_email)
            self.buttons.append(button)

            if len(self.buttons) > 1:
                old_button = self.buttons.pop(0)
                old_button.destroy()
    def default_widgets(self):
        entry_email = Entry(self)
        entry_email.grid(column=0,row=1)

        entry_date = Entry(self)
        entry_date.grid(column=1, row=1)

        send_button = Button(self,text='odeslat mail',
                                 command=partial(self.send_email, self.email_entries, self.date_entries))
        send_button.grid(column=1, row=len(self.email_entries) + 2)

        self.buttons.append(send_button)
        self.date_entries.append(entry_date)
        self.email_entries.append(entry_email)