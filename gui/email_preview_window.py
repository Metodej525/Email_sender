from tkinter import Label, Frame, Button
from tkhtmlview import HTMLLabel
import tkinter as tk



class EmailPreviewTab(Frame):
    """
    Tkinter záložka pro náhled e-mailu.
    Načítá hodnoty z konfigurace a automaticky je nahrazuje.
    """

    # Slovník definuje popisky jednotlivých údajů a odpovídající klíče v konfiguraci.
    FIELDS = {'from':('Od: ','sender_email'),
              'to':('Komu: ','receiver_email'),
              'subject':('Předmět: ','subject'),
              'preview':('Náhled: ','')
              }

    def __init__(self,notebook,load_email_details,html_converter,config, importance_toggle):
        # Inicializace základního Tkinter Frame widgetu.
        super().__init__(notebook)

        # Načtení údajů e-mailu z konfigurace.
        self.load_email_details = load_email_details(config)
        self.html_converter = html_converter
        self.importance_toggle = importance_toggle

        # Vytvoření tlačítka pro přepínání šablony podle důležitosti.
        skull_btn = SkullPreviewToggle(self,self.switch_template)
        skull_btn.grid(column=0,row=0,sticky="nw",padx=25,pady=5)

        # Vytvoření popisků a hodnot podle definice ve slovníku FIELDS.
        for row, (key, (label_text, config_text)) in enumerate(self.FIELDS.items()):
            Label(self,text=label_text).grid(column=0,row=row + 1,sticky="nw",padx=5,pady=5)

            # Načtení odpovídající hodnoty z konfigurace; při chybějící hodnotě se použije prázdný řetězec.
            config_value = config.get('EMAIL', config_text, fallback='')
            Label(self,text=config_value).grid(column=1,row=row + 1,sticky="nw",padx=5,pady=5)

        # Převod těla e-mailu do HTML podoby pro zobrazení v náhledu.
        self.raw_html = self.html_converter(self.load_email_details['body'])

        # Vytvoření HTML widgetu a jeho umístění do záložky.
        self.email_label = HTMLLabel(self, html=self.raw_html, height=100, width=100)
        self.email_label.grid(column=1, row=4, padx=25, pady=0)



    def switch_template(self,state):
        # Úprava HTML šablony podle aktuálního stavu důležitosti.
        email_template = self.importance_toggle(self.raw_html,state)

        # Odstranění původního náhledu před vytvořením nového.
        self.email_label.destroy()

        # Vytvoření a zobrazení aktualizovaného náhledu e-mailu.
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

        # Nastavení výchozího stavu přepínače.
        self.state = 1

        # Při kliknutí na tlačítko se zavolá metoda cycle.
        self.config(command=self.cycle)

        self.master = master
        self.switch_template = switch_template

    def cycle(self):
        # Přepínání mezi třemi stavy; po třetím stavu se vrací zpět na první.
        if self.state >= 3:
            self.state = 1
        else:
            self.state += 1

        # Předání nového stavu pro aktualizaci náhledu e-mailu.
        self.switch_template(self.state)

        # Aktualizace vzhledu tlačítka podle aktuálního stavu.
        self.update_style()

    def update_style(self):
        """Nastaví vizuální styl tlačítka podle aktuálního stavu."""

        # První stav – šedé pozadí a běžný vzhled tlačítka.
        if self.state == 1:
            self.config(
                text="💀",
                bg="#eeeeee",
                activebackground="#eeeeee",
                fg="black",
                relief="raised"
            )

        # Druhý stav – žluté pozadí.
        elif self.state == 2:
            self.config(
                text="💀",
                bg="#fff59d",
                activebackground="#fff59d",
                fg="black",
                relief="groove"
            )

        # Třetí stav – tmavě červené pozadí a bílé písmo.
        elif self.state == 3:
            self.config(
                text="💀",
                bg="#8e2430",
                activebackground="#8e2430",
                fg="white",
                relief="sunken"
            )
