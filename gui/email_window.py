from dataclasses import dataclass
from tkinter import Frame, Button, Entry, Label, StringVar, Listbox
import tkinter as tk
import tkinter.messagebox
from tkhtmlview import HTMLLabel



class EmailTab(Frame):
    def __init__(self, notebook, root, excel_search, config,
                 selected_value_manager,html_converter,
                 EmailSendManager, email_details, EmailConstructor, importance_toggle, app_state):
        super().__init__(notebook)

        # --- Stav a závislosti záložky ---
        self.rows = []                         # Seznam vytvořených instancí EmailRow.
        self.root = root                       # Reference na hlavní okno (kvůli Toplevel a událostem).
        self.config = config
        self.excel_search = excel_search       # Callback pro vyhledávání v Excel datech.
        self.importance_toggle = importance_toggle
        self.btn_send_email = None
        self.selected_value_manager = selected_value_manager
        self.html_converter = html_converter
        self.EmailSendManager = EmailSendManager
        self.EmailConstructor = EmailConstructor
        self.dropdown = None                    # Aktuálně otevřené našeptávací okno.
        self.toolbox()
        self.default_row()
        self.email_details = email_details
        self.app_state = app_state




    def toolbox(self):
        """Vytvoří popisky v horní části záložky."""
        Label(self, text='Email').grid(column=0, row=0, pady=5, padx=25)
        # Label (self, text='Datum vypršení certifikátu').grid(column=1, row=0, pady=5, padx=75)

    def default_row(self):
        """Inicializuje první (výchozí) řádek."""
        # Vytvoření prvního řádku a předání potřebných callbacků a závislostí.
        row = EmailRow( self, self.config,
                        self.remove_row,
                        self.EmailConstructor,
                        self.html_converter,
                        self.root,
                        self.importance_toggle
                       )
        row.grid(row=len(self.rows) + 1, column=0, columnspan=6, sticky="w")

        self.rows.append(row)

        # První řádek nemá tlačítko pro odstranění.
        if hasattr(self.rows[0],'btn_delete'):
            self.rows[0].btn_delete.destroy()

        # Pokud již existuje tlačítko pro odeslání, odstraní se před vytvořením nového.
        if self.btn_send_email:
            self.btn_send_email.destroy()

        # Vytvoření tlačítka pro přidání dalšího řádku a tlačítka pro odeslání.
        self.create_add_email_btn()
        self.create_send_btn(2)

    def create_add_email_btn(self):
        # Tlačítko s ikonou plus přidává další e-mailový řádek.
        self.add_email_btn = Button(self, text='➕', command=self.add_email)
        self.add_email_btn.grid(row=1,column=6, padx= 0)

    def add_email(self):
        """Přidá nový e-mailový řádek (maximálně 5)."""

        row = None

        # Kontrola maximálního počtu řádků.
        if len(self.rows) < 5:
            row = EmailRow(
                self,
                self.config,
                self.remove_row,
                self.EmailConstructor,
                self.html_converter,
                self.root,
                self.importance_toggle
            )

            # Uložení nového řádku do seznamu a jeho umístění v rozhraní.
            self.rows.append(row)
            row.grid(row=len(self.rows) + 1, column=0, columnspan=5, sticky="w")

        # Aktualizace pozice tlačítka pro odeslání podle aktuálního počtu řádků.
        if self.btn_send_email:
            self.btn_send_email.destroy()
            self.create_send_btn(len(self.rows) + 3)

        self.check_add_email_btn_grid()

        return row

    def check_add_email_btn_grid(self):

        # Zjištění, zda existuje alespoň jeden prázdný a alespoň jeden vyplněný řádek.
        has_empty = any(not row.entry_email.get().strip() for row in self.rows)
        has_filled = any(row.entry_email.get().strip() for row in self.rows)

        # Pokud jsou současně prázdné i vyplněné řádky, tlačítko pro přidání se skryje.
        if has_empty and has_filled:
            self.add_email_btn.grid_remove()
        else:
            self.add_email_btn.grid()

    def create_send_btn(self, row):
        """Vytvoří tlačítko pro odeslání e-mailů."""
        self.btn_send_email = Button(self, text='Odeslat email', command=self.send_email)
        self.btn_send_email.grid(column=0, row=row, pady=20)

    def remove_row(self, row):
        """Odstraní konkrétní řádek a přepočítá rozložení prvků."""
        # Odstranění widgetu z grafického rozhraní a ze seznamu řádků.
        row.destroy()
        self.rows.remove(row)

        # Opětovné rozmístění zbývajících řádků od začátku.
        for i, r in enumerate(self.rows):
            r.grid_configure(row=i + 1)

        # Aktualizace pozice tlačítka pro odeslání.
        if self.btn_send_email:
            self.btn_send_email.destroy()
        self.create_send_btn(len(self.rows) + 1)
        self.check_add_email_btn_grid()

    def send_email(self):
        """Zobrazí potvrzení a následně zajistí odeslání e-mailů."""
        # Před odesláním se uživatele zeptá na potvrzení akce.
        if tkinter.messagebox.askquestion(title='', message='Odeslat email?') == 'yes':
            self._pop_up_window('', 'Email byl odeslán')

            # Získání dat pouze z řádků, které mají vyplněnou e-mailovou adresu.
            data = [
                row.set_data()
                for row in self.rows
                if row.email and row.email.strip()
            ]

            # Sestavení těla e-mailu pro jednotlivé záznamy.
            self.EmailConstructor(self.config,data, self.importance_toggle).set_email_body()

            # Vytvoření správce odesílání a spuštění odeslání e-mailů.
            sender = self.EmailSendManager(self.config,data,self.email_details)
            sender.email_sender()

            # Po odeslání se formulář vrátí do výchozího stavu.
            self.reset_rows()

    def reset_rows(self):
        """Vrátí grafické rozhraní do výchozího stavu."""
        # Odstranění všech aktuálně vytvořených řádků.
        for row in self.rows:
            row.destroy()

        self.rows.clear()
        self.default_row()

    def on_search_change(self, row):
        """Spustí živé vyhledávání při změně textu v e-mailovém poli."""
        # Vyhledávání se spouští pouze pro řádek, který stále existuje.
        if row in self.rows:
            email_val = str(row.entry_email.get().lower())

            # Vyhledávání se spustí až po zadání alespoň tří znaků.
            if len(email_val) >= 3:
                self.live_search(email_val, row)
    def live_search(self, entry_val, row):
        """Vytvoří našeptávací seznam odpovídajících záznamů."""

        # Vyhledání odpovídajících záznamů v aktuálním DataFrame.
        values = self.excel_search(entry_val, self.app_state.get_df())

        # Pokud nebyly nalezeny žádné výsledky, případný dropdown se zavře.
        if not values:
            if self.dropdown:
                self.dropdown.destroy()
                self.dropdown = None
            return

        # Uložení řádku, ke kterému aktuální našeptávač patří.
        self.active_row = row

        # Převod jednotlivých záznamů na textové řetězce pro zobrazení v Listboxu.
        stripped_values_list = [
            ', '.join(map(str, row_data))
            for row_data in values
        ]

        # Odstranění předchozího našeptávacího okna.
        if self.dropdown:
            self.dropdown.destroy()

        # Vytvoření nového vyskakovacího okna pro našeptávač.
        self.dropdown = EmailDropDownMenu(self.root, row, self)

        # Vytvoření Listboxu; jeho výška se přizpůsobí počtu výsledků, maximálně na 5.
        self.dropdown.listbox = Listbox(
            self.dropdown,
            width=50,
            height=min(5, len(stripped_values_list))
        )
        self.dropdown.listbox.pack(fill="both", expand=True)

        # Vložení maximálně pěti nalezených výsledků do seznamu.
        for val in stripped_values_list[:5]:
            self.dropdown.listbox.insert(tk.END, val)

        # Automatické označení prvního výsledku.
        self.dropdown.listbox.selection_set(0)
        self.dropdown.listbox.activate(0)

        # Při dvojkliku na výsledek se zavolá metoda pro jeho výběr.
        self.dropdown.listbox.bind(
            "<Double-Button-1>",
            lambda event: self.on_select(event)
        )

        # Registrace události kliknutí mimo okno pro případné zavření dropdownu.
        self.root.bind(
            "<Button-1>",
            self.dropdown.on_click_outside,
            add="+"
        )

    def focus_dropdown(self, row):
        # Pokud dropdown existuje, předá se fokus jeho Listboxu a označí se první položka.
        if self.dropdown and hasattr(self.dropdown, "listbox"):
            self.dropdown.listbox.focus_set()
            self.dropdown.listbox.selection_set(0)

    def on_select(self, event=None ):
        # Pokud není otevřený dropdown, není co vybírat.
        if not self.dropdown:
            return

        # Určení Listboxu, ze kterého se má načíst vybraná položka.
        if event is not None and event.keysym != "Return":
            lb = event.widget
        else:
            lb = self.dropdown.listbox
        selection = lb.curselection()

        # Pokud není označena žádná položka, metoda se ukončí.
        if not selection:
            return

        # Načtení textu vybrané položky.
        value = lb.get(selection[0])

        # Získání řádku, pro který uživatel provedl výběr.
        row = self.active_row

        # Pokud se vybírá v posledním řádku, připraví se další řádek.
        if self.rows.index(self.active_row) == len(self.rows) -1:
            statement = self.add_email()
            if statement:
                self.refocus_entry(statement)

        # Zavření našeptávacího okna po výběru.
        self.dropdown.safe_destroy()

        # Zpracování vybrané hodnoty a rozdělení údajů na e-mail, datum a čas.
        email, exp_date, exp_time = self.selected_value_manager(value)

        # Vyplnění údajů do vybraného řádku a aktualizace jeho datového objektu.
        row.safe_set_values(email, exp_date, exp_time)
        row.set_data()

    def refocus_entry(self,row):
        # Přesunutí fokusu do e-mailového pole nově vytvořeného řádku.
        row.entry_email.focus_set()

    @staticmethod
    def _pop_up_window(title, text):
        # Zobrazení informačního dialogového okna.
        tkinter.messagebox.showinfo(title=title, message=text)

class EmailRow(Frame):
    """
    Reprezentuje jeden řádek v EmailTab.
    Obsahuje:
    - Entry pro email s live search
    - Label pro datum - automaticky se načte po zvolení z dropdown menu
    - Tlačítko pro smazání řádku
    - Tlačítko pro náhled / preview emailu
    """

    def __init__(self, parent, config, remove_callback, EmailConstructor, html_converter,root, importance_toggle):
        super().__init__(parent)

        # --- internal state ---
        self.root = root
        self._after_id = None               # ID naplánované události pro debounce.
        self.is_updating = False            # Příznak, který zabraňuje spuštění vyhledávání při programové změně Entry.
        self.search_email_var = StringVar() # Proměnná propojující Entry s živým vyhledáváním.
        self.exp_date = None
        self.exp_time = None
        self.email = None
        self.parent = parent
        self.config = config
        self.focus_dropdown_callback = parent.focus_dropdown
        self.EmailConstructor = EmailConstructor
        self.html_converter = html_converter
        self.importance_toggle = importance_toggle

        # Datový objekt uchovávající údaje konkrétního e-mailového řádku.
        self.data = EmailData(exp_time='',
                         exp_date='',
                         email='',
                         importance=1,
                         email_body='')
        # ------------------------------
        # Debounce callback pro live search
        # ------------------------------
        def trace_callback(*args):
            # Při programové aktualizaci hodnoty se vyhledávání nespustí.
            if self.is_updating:
                return

            # Zrušení předchozí naplánované události, pokud ještě čeká na spuštění.
            if self._after_id:
                self.after_cancel(self._after_id)

            # Vyhledávání se naplánuje až 200 ms po poslední změně textu.
            self._after_id = self.after(
                200, lambda: parent.on_search_change(self))

        # Připojení callbacku k události změny hodnoty StringVar.
        self.search_email_var.trace_add("write", trace_callback)

        # ------------------------------
        # Grafické komponenty řádku.
        # ------------------------------

        # Vstupní pole pro e-mail propojené s proměnnou StringVar.
        self.entry_email = Entry(self, width=25,textvariable=self.search_email_var)
        self.entry_email.grid(column=0, row=0, padx=5, pady=5)

        # Klávesové zkratky pro pohyb v našeptávači a potvrzení výběru.
        self.entry_email.bind("<Down>", self.on_down)
        self.entry_email.bind("<Return>", self.on_enter)

        # Popisek pro zobrazení data a času expirac
        self.label_date = Label(self, text='')
        self.label_date.grid(column=1, row=0, padx=15, pady=5)

        # Tlačítko pro zobrazení náhledu sestaveného e-mailu.
        self.btn_preview = Button(self, text="🔎", command=self.email_preview)
        self.btn_preview.grid(column=2, row=0)

        # Přepínač důležitosti e-mailu.
        self.btn_importance = SkullToggle(self,self.data)
        self.btn_importance.grid(column=3,row=0)

        # Tlačítko pro odstranění řádku; předává aktuální instanci callbacku rodičovské třídy.
        self.btn_delete = Button(self, text="x", command=lambda: remove_callback(self))
        self.btn_delete.grid(column=4, row=0)

    def email_preview(self):
        """Vytvoří náhled e-mailu pro aktuální řádek."""
        # Sestavení těla e-mailu a uložení výsledku do datového objektu.
        self.EmailConstructor(self.config,self.data, self.importance_toggle).set_email_body()
        text = self.data.email_body

        # Převod textu e-mailu do HTML podoby.
        converted_text = self.html_converter(text)

        # Vytvoření samostatného vyskakovacího okna s náhledem.
        popup = tk.Toplevel(self.parent)
        popup.wm_title("🔎")

        HTMLLabel(popup, html=converted_text,height=30,padx=25,pady=25).pack()

    def on_enter(self,event):
        # Předání události Enter rodičovské třídě, která zpracuje výběr z dropdownu.
        self.parent.on_select(event)

    def on_down(self, event):
        # Při stisku šipky dolů se fokus přesune do našeptávacího seznamu.
        if self.parent.dropdown:
            self.parent.dropdown.listbox.focus_set()
            self.parent.dropdown.listbox.selection_clear(0, "end")
            self.parent.dropdown.listbox.selection_set(0)
            self.parent.dropdown.listbox.activate(0)

        # Zabrání standardnímu zpracování události klávesy v Entry.
        return "break"

    def safe_set_values(self, email, exp_date, exp_time):
        # Dočasné vypnutí reakce na změnu StringVar během programového vyplňování.
        self.is_updating = True
        try:
            self.email = email
            self.exp_date = exp_date
            self.exp_time = exp_time

            # Aktualizace textu v e-mailovém poli
            self.entry_email.delete(0, tk.END)
            self.entry_email.insert(0, self.email)

            # Zobrazení data a času expirace v popisku.
            self.label_date.config(text=f"{exp_date} {exp_time}")
        finally:
            # Příznak se vrátí do původního stavu i v případě chyby.
            self.is_updating = False
    def set_data(self):
        # Přenos aktuálních hodnot z řádku do datového objektu EmailData.
        self.data.email = self.email
        self.data.exp_date = self.exp_date
        self.data.exp_time = self.exp_time

        # Vrácení aktualizovaného datového objektu.
        return self.data


class EmailDropDownMenu(tk.Toplevel):

    def __init__(self, root, row, parent):
        super().__init__(root)

        self.root = root
        self.row = row
        self.parent = parent

        # Odstranění standardního titulkového pruhu okna.
        self.wm_overrideredirect(True)

        # Nastavení okna tak, aby zůstávalo nad ostatními okny.
        self.attributes("-topmost", True)

        # Umístění dropdownu pod vstupní pole příslušného řádku.
        self.update_position()

        # Reakce na přesunutí, minimalizaci okna, změnu záložky a klávesové události.
        self.root.bind("<Configure>", self._on_window_move, add="+")
        self.root.bind("<Unmap>", self._on_minimize, add="+")
        self.root.bind("<<NotebookTabChanged>>", self._on_tab_change, add="+")
        self.bind("<Return>", self.on_enter)
        self.root.bind("<Button-1>", self.on_click_outside)

    # =========================
    # POSITION
    # =========================

    def on_enter(self, event):
        # Předání potvrzení výběru rodičovské třídě.
        if self.parent.dropdown:
            self.parent.on_select(event)

        # Zabránění dalšímu standardnímu zpracování klávesy Enter.
        return "break"
    def update_position(self):

        try:
            # Získání vodorovné souřadnice vstupního pole na obrazovce.
            x = self.row.entry_email.winfo_rootx()

            # Výpočet svislé souřadnice těsně pod vstupním polem.
            y = (
                self.row.entry_email.winfo_rooty()
                + self.row.entry_email.winfo_height()
            )

            # Nastavení pozice vyskakovacího okna.
            self.geometry(f"+{x}+{y}")

        except tk.TclError:
            # Ignorování chyby, pokud již příslušný Tkinter widget neexistuje.
            pass

    def _on_window_move(self, event):
        # Při změně pozice nebo velikosti hlavního okna se aktualizuje pozice dropdownu.
        self.update_position()

    # =========================
    # CLOSE EVENTS
    # =========================

    def _on_minimize(self, event):
        # Zavření dropdownu při minimalizaci hlavního okna.
        self.safe_destroy()

    def _on_tab_change(self, event):
        # Zavření dropdownu při přepnutí na jinou záložku.
        self.safe_destroy()

    def on_click_outside(self, event):

        try:
            widget = event.widget

            # Pokud uživatel klikne uvnitř dropdownu, okno zůstane otevřené.
            if str(widget).startswith(str(self)):
                return

            # Kliknutí do vstupního pole také nezpůsobí zavření dropdownu.
            if widget == self.row.entry_email:
                return

            # Kliknutí mimo dropdown a vstupní pole způsobí jeho zavření.
            self.safe_destroy()

        except tk.TclError:
            # Ošetření situace, kdy již některý z widgetů neexistuje.
            pass

    # =========================
    # BEZPEČNÉ ODSTRANĚNÍ OKNA
    # =========================

    def safe_destroy(self):

        try:
            self.destroy()

        except tk.TclError:
            # Ošetření chyby při pokusu odstranit již zrušené okno.
            pass

class SkullToggle(tk.Button):
    """
        Vlastní Tkinter button fungující jako toggle přepínač.

        Button mění svůj vizuální stav po kliknutí:
        - vypnutý stav = šedé pozadí
        - zapnutý stav = žluté pozadí
        """
    def __init__(self, master,data, **kwargs):
        # Inicializace základního Tkinter Button widgetu.
        super().__init__(master, text="💀", width=4, **kwargs)

        self.data = data
        self.state = 1

        # Při kliknutí se zavolá metoda cycle s datovým objektem aktuálního řádku.
        self.config(command=lambda: self.cycle(self.data))
        self.master = master


    def cycle(self,data):
        # Přepínání mezi třemi stavy; po třetím stavu se přechází zpět na první.
        if self.state >= 3:
            self.state = 1
        else:
            self.state += 1

        # Aktualizace vzhledu tlačítka a uložení nové hodnoty důležitosti.
        self.update_style()
        self.set_state(data)


    def update_style(self):
        """Nastaví vizuální styl tlačítka podle aktuálního stavu."""
        # První stav – šedé pozadí.
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
    def set_state(self,data):
        # Uložení aktuálního stavu přepínače do atributu importance datového objektu.
        data.importance = self.state

@dataclass
class EmailData:
    """
      Datová třída uchovávající údaje e-mailu pro service vrstvu.
      Instance se vytváří společně s každým EmailRow.
      """
    # Datové atributy jednoho e-mailového záznamu.
    exp_date: str
    exp_time: str
    email_body: str
    email: str
    importance:int

