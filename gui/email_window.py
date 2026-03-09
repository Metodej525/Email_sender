from tkinter import Frame, Button, Entry, Label , StringVar
from functools import partial



class EmailTab(Frame):
    def __init__(self,notebook, send_email):
        super().__init__(notebook)
        self.send_email = send_email

        Label(self, text='emailová schránka').grid(column=0,row=0)
        Label(self,text='datum ukončení certifikátu').grid(column=1,row=0)

        notebook.add(self, text='Email')
        self.add_email_button = Button(self, text='přidej email', command=partial(self.add_email_receiver))
        self.add_email_button.grid(column=2, row=1)
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
        #kontrola widgetu odeslat email, aby se nevytvoril znovu
        if not hasattr(self, 'add_email_button') or not self.add_email_button.winfo_exists():
            self.add_email_button = Button(self, text='přidej email', command=partial(self.add_email_receiver))
            self.add_email_button.grid(column=2, row=1)
        # else:
        #     print('button už tam je')
        self.buttons.append(send_button)
        self.date_entries.append(entry_date)
        self.email_entries.append(entry_email)
    def live_search(self):

        pass
    def reset_tab(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.default_widgets()