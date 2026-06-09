from tkinter import Label, Frame, Button
from tkhtmlview import HTMLLabel
import tkinter as tk



class EmailPreviewTab(Frame):
    """
        Tkinter tab for email preview.

        Loads values from config and automatically replaces them.
        """
    FIELDS = {'from':('Od: ','sender_email'),
              'to':('Komu: ','receiver_email'),
              'subject':('Předmět: ','subject'),
              'preview':('Náhled: ','')
              }

    def __init__(self,notebook,load_email_details,html_converter,config, importance_toggle):
        super().__init__(notebook)
        self.load_email_details = load_email_details(config)
        self.html_converter = html_converter
        self.importance_toggle = importance_toggle

        skull_btn = SkullPreviewToggle(self,self.switch_template)
        skull_btn.grid(column=0,row=0,sticky="nw",padx=25,pady=5)
        for row, (key, (label_text, config_text)) in enumerate(self.FIELDS.items()):
            Label(self,text=label_text).grid(column=0,row=row + 1,sticky="nw",padx=5,pady=5)
            config_value = config.get('EMAIL', config_text, fallback='')
            Label(self,text=config_value).grid(column=1,row=row + 1,sticky="nw",padx=5,pady=5)

        self.raw_html = self.html_converter(self.load_email_details['body'])

        self.email_label = HTMLLabel(self, html=self.raw_html, height=100, width=100)
        self.email_label.grid(column=1, row=4, padx=25, pady=0)



    def switch_template(self,state):
        email_template = self.importance_toggle(self.raw_html,state)
        self.email_label.destroy()
        self.email_label = HTMLLabel(self, html=email_template, height=100, width=100)
        self.email_label.grid(column=1, row=4, padx=25, pady=0)

class SkullPreviewToggle(tk.Button):
    """
        Vlastní Tkinter button fungující jako toggle přepínač.

        Button mění svůj vizuální stav po kliknutí:
        - vypnutý stav = šedé pozadí
        - zapnutý stav = žluté pozadí
        """

    def __init__(self, master, switch_template, **kwargs):
        # inicializace základního Tkinter Button widgetu
        super().__init__(master, text="💀", width=4, **kwargs)

        self.state = 1
        self.config(command=self.cycle)
        self.master = master
        self.switch_template = switch_template

    def cycle(self):

        if self.state >= 3:
            self.state = 1
        else:
            self.state += 1
        self.switch_template(self.state)
        self.update_style()

    def update_style(self):
        """
            Nastaví vizuální styl buttonu podle aktuálního stavu.
            """
        if self.state == 1:
            self.config(
                text="💀",
                bg="#eeeeee",
                activebackground="#eeeeee",
                fg="black",
                relief="raised"
            )
        elif self.state == 2:
            self.config(
                text="💀",
                bg="#fff59d",
                activebackground="#fff59d",
                fg="black",
                relief="groove"
            )
        elif self.state == 3:
            self.config(
                text="💀",
                bg="#8e2430",
                activebackground="#8e2430",
                fg="white",
                relief="sunken"
            )
