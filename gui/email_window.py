from tkinter import Frame, Button, Entry, Label
from functools import partial



class EmailTab(Frame):
    def __init__(self,notebook, send_email):
        super().__init__(notebook)

        self.send_email = send_email
        notebook.config(width=500,height=100)
        Label(self, text='emailová schránka').grid(column=0,row=0,sticky="nw",padx=5, pady=5)
        Label(self,text='datum ukončení certifikátu').grid(column=1,row=0,sticky="nw",padx=5, pady=5)
        self.columnconfigure(3, weight=1)
        notebook.add(self, text='Email')
        self.add_email_button = Button(self, text='přidej email', command=partial(self.add_email_receiver))
        self.add_email_button.grid(column=2, row=1)

        self.buttons = []
        self.email_entries = []
        self.date_entries = []
        self.delete_email_buttons = []
        self.email_preview_buttons = []

        self.default_widgets()

    def add_email_receiver(self):
        if len(self.email_entries) < 5:
            row = len(self.email_entries) + 1
            entry_email = Entry(self)
            entry_email.grid(column=0, row=row,sticky="nw",padx=5, pady=5)

            entry_date = Entry(self)
            entry_date.grid(column=1, row=row,sticky="nw",padx=5, pady=5)
            button = Button(self,
                                 text='odeslat mail',
                                 command=partial(self.send_email,
                                                 self.email_entries,
                                                 self.date_entries,
                                                 self.delete_email_buttons,
                                                 self.email_preview_buttons
                                                 )
                            )
            button.grid(column=1, row=row + 1)

            button_email_delete = Button(self,text='x')
            button_email_delete.grid(column=2, row=row,sticky="nw",padx=5, pady=5)

            button_email_preview = Button(self,text='🔎')
            button_email_preview.grid(column=3, row=row,sticky="nw",padx=5, pady=5)

            self.date_entries.append(entry_date)
            self.email_entries.append(entry_email)
            self.buttons.append(button)
            self.delete_email_buttons.append(button_email_delete)
            self.email_preview_buttons.append(button_email_preview)

            if len(self.buttons) > 1:
                old_button = self.buttons.pop(0)
                old_button.destroy()

    def default_widgets(self):
        entry_email = Entry(self)
        entry_email.grid(column=0,row=1,sticky="nw",padx=5, pady=5)

        entry_date = Entry(self)
        entry_date.grid(column=1, row=1,sticky="nw",padx=5, pady=5)

        send_button = Button(self,text='odeslat mail',
                                 command=partial(self.send_email,
                                                 self.email_entries,
                                                 self.date_entries,
                                                 self.delete_email_buttons,
                                                 self.email_preview_buttons
                                                 )
                             )
        send_button.grid(column=1, row=len(self.email_entries) + 2)
        #Kontrola widgetu odeslat email, aby se nevytvoril znovu
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

        self.buttons.clear()
        self.email_entries.clear()
        self.date_entries.clear()

        self.default_widgets()

    def delete_row(self,delete_button):
        info = delete_button.grid_info()
        row = info['row'] - 2
        self.delete_email_buttons.remove(delete_button)

