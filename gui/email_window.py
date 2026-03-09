from tkinter import Frame, Button, Entry, Label , StringVar
from functools import partial
from tkhtmlview import HTMLLabel


class EmailTab(Frame):
    def __init__(self,notebook, send_email, load_email_details,config):
        super().__init__(notebook)
        self.send_email = send_email
        self.load_email_details = load_email_details(config)
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
        #Náhled mailu
        html = self.load_email_details['body'].encode('cp1250').decode('utf-8', errors='ignore')
        # Převod dvojitých novinek na odstavce
        html = html.replace('\r\n\r\n', '</p><p>')
        html = html.replace('\n\n', '</p><p>')

        # Převod jednotlivých nových řádků na <br>
        html = html.replace('\r\n', '<br>')
        html = html.replace('\n', '<br>')

        # Obal pro celý text do <p>
        html = f"<p>{html}</p>"
        email_label = HTMLLabel(self, html=html)
        email_label.grid(column=3, row=0)

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