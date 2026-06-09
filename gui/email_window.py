from dataclasses import dataclass
from tkinter import Frame, Button, Entry, Label, StringVar, Listbox
import tkinter as tk
import tkinter.messagebox
from tkhtmlview import HTMLLabel



class EmailTab(Frame):
    def __init__(self, notebook, root, excel_search, config,
                 df,selected_value_manager,html_converter,
                 EmailSendManager, email_details, EmailConstructor, importance_toggle):
        super().__init__(notebook)

        # --- state ---
        self.rows = []                         # list of EmailRow instances
        self.root = root                       # reference na root (kvůli Toplevel, bindům)
        self.config = config
        self.excel_search = excel_search       # callback pro live search
        self.df = df
        self.importance_toggle = importance_toggle
        self.btn_send_email = None
        self.selected_value_manager = selected_value_manager
        self.html_converter = html_converter
        self.EmailSendManager = EmailSendManager
        self.EmailConstructor = EmailConstructor
        self.dropdown = None
        self.toolbox()
        self.default_row()
        self.email_details = email_details





    def toolbox(self):
        """Header labels"""
        Label(self, text='Email').grid(column=0, row=0, pady=5, padx=25)
        # Label(self, text='Datum vypršení certifikátu').grid(column=1, row=0, pady=5, padx=75)

    def default_row(self):
        """Inicializuje první (defaultní) řádek"""
        row = EmailRow( self, self.config,
                        self.remove_row,
                        self.EmailConstructor,
                        self.html_converter,
                        self.root,
                        self.importance_toggle
                       )
        row.grid(row=len(self.rows) + 1, column=0, columnspan=6, sticky="w")

        self.rows.append(row)

        # první řádek nemá delete tlačítko
        if hasattr(self.rows[0],'btn_delete'):
            self.rows[0].btn_delete.destroy()

        # reset send buttonu
        if self.btn_send_email:
            self.btn_send_email.destroy()

        #vytvoení send buttonu na 3 řádku
        self.create_add_email_btn()
        self.create_send_btn(2)

    def create_add_email_btn(self):
        self.add_email_btn = Button(self, text='➕', command=self.add_email)
        self.add_email_btn.grid(row=1,column=6, padx= 0)

    def add_email(self):
        """Přidá nový emailový řádek (max 5)"""

        row = None

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

            self.rows.append(row)
            row.grid(row=len(self.rows) + 1, column=0, columnspan=5, sticky="w")

        # vždy update buttonu (NEblokuje return)
        if self.btn_send_email:
            self.btn_send_email.destroy()
            self.create_send_btn(len(self.rows) + 3)

        self.check_add_email_btn_grid()

        return row

    def check_add_email_btn_grid(self):

        has_empty = any(not row.entry_email.get().strip() for row in self.rows)
        has_filled = any(row.entry_email.get().strip() for row in self.rows)

        if has_empty and has_filled:
            self.add_email_btn.grid_remove()
        else:
            self.add_email_btn.grid()

    def create_send_btn(self, row):
        """Vytvoří tlačítko pro odeslání"""
        self.btn_send_email = Button(self, text='Odeslat email', command=self.send_email)
        self.btn_send_email.grid(column=0, row=row, pady=20)

    def remove_row(self, row):
        """Smaže konkrétní řádek a přepočítá layout"""
        row.destroy()
        self.rows.remove(row)

        # reindex gridu
        for i, r in enumerate(self.rows):
            r.grid_configure(row=i + 1)

        # reposition send button
        if self.btn_send_email:
            self.btn_send_email.destroy()
        self.create_send_btn(len(self.rows) + 1)
        self.check_add_email_btn_grid()

    def send_email(self):
        """Potvrzení a odeslání emailu"""
        if tkinter.messagebox.askquestion(title='', message='Odeslat email?') == 'yes':
            self._pop_up_window('', 'Email byl odeslán')
            data = [
                row.set_data()
                for row in self.rows
                if row.email and row.email.strip()
            ]
            self.EmailConstructor(self.config,data, self.importance_toggle)
            sender = self.EmailSendManager(self.config,data,self.email_details)
            sender.email_sender()
            self.reset_rows()

    def reset_rows(self):
        """Reset UI do výchozího stavu"""
        for row in self.rows:
            row.destroy()

        self.rows.clear()
        self.default_row()

    def on_search_change(self, row):
        """Trigger live search (debounced z EmailRow)"""
        if row in self.rows:
            email_val = str(row.entry_email.get().lower())
            if len(email_val) >= 3:
                self.live_search(email_val, row)

    def live_search(self, entry_val, row):
        """Vykreslí autocomplete dropdown"""

        values = self.excel_search(entry_val, self.df)
        # nic nenalezeno → zavři dropdown
        if not values:
            if self.dropdown:
                self.dropdown.destroy()
                self.dropdown = None
            return

        # aktivní row
        self.active_row = row

        # transformace dat do stringu
        stripped_values_list = [
            ', '.join(map(str, row_data))
            for row_data in values
        ]

        # zruš starý dropdown
        if self.dropdown:
            self.dropdown.destroy()

        # vytvoř nový dropdown
        self.dropdown = EmailDropDownMenu(self.root, row, self)

        # Listbox
        self.dropdown.listbox = Listbox(
            self.dropdown,
            width=50,
            height=min(5, len(stripped_values_list))
        )
        self.dropdown.listbox.pack(fill="both", expand=True)

        # vložení hodnot
        for val in stripped_values_list[:5]:
            self.dropdown.listbox.insert(tk.END, val)

        self.dropdown.listbox.selection_set(0)
        self.dropdown.listbox.activate(0)
        # select event
        self.dropdown.listbox.bind(
            "<Double-Button-1>",
            lambda event: self.on_select(event)
        )

        # click outside
        self.root.bind(
            "<Button-1>",
            self.dropdown.on_click_outside,
            add="+"
        )

    def focus_dropdown(self, row):
        if self.dropdown and hasattr(self.dropdown, "listbox"):
            self.dropdown.listbox.focus_set()
            self.dropdown.listbox.selection_set(0)
    def on_select(self, event=None ):
        if not self.dropdown:
            return

        if event is not None and event.keysym != "Return":
            lb = event.widget
        else:
            lb = self.dropdown.listbox
        selection = lb.curselection()

        if not selection:
            return

        value = lb.get(selection[0])

        row = self.active_row

        if self.rows.index(self.active_row) == len(self.rows) -1:
            statement = self.add_email()
            if statement:
                self.refocus_entry(statement)
        self.dropdown.safe_destroy()

        email, exp_date, exp_time = self.selected_value_manager(value)

        row.safe_set_values(email, exp_date, exp_time)
        row.set_data()
    def refocus_entry(self,row):
        row.entry_email.focus_set()
    @staticmethod
    def _pop_up_window(title, text):
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
        self._after_id = None               # uchovává ID 'after' pro debounce
        self.is_updating = False  # flag pro regulaci trace_callback
        self.search_email_var = StringVar() # propojení Entry ↔ live search
        self.exp_date = None
        self.exp_time = None
        self.email = None
        self.parent = parent
        self.config = config
        self.focus_dropdown_callback = parent.focus_dropdown
        self.EmailConstructor = EmailConstructor
        self.html_converter = html_converter
        self.importance_toggle = importance_toggle
        self.data = EmailData(exp_time='',
                         exp_date='',
                         email='',
                         importance=1,
                         email_body='')
        # ------------------------------
        # Debounce callback pro live search
        # ------------------------------
        def trace_callback(*args):
            if self.is_updating:
                return

            if self._after_id:
                self.after_cancel(self._after_id)

            self._after_id = self.after(
                200, lambda: parent.on_search_change(self))
        # připojení callbacku na změnu StringVar
        self.search_email_var.trace_add("write", trace_callback)

        # ------------------------------
        # UI komponenty
        # ------------------------------

        # Entry pro email
        self.entry_email = Entry(self, width=25,textvariable=self.search_email_var)
        self.entry_email.grid(column=0, row=0, padx=5, pady=5)

        self.entry_email.bind("<Down>", self.on_down)
        self.entry_email.bind("<Return>", self.on_enter)

        # Label – placeholder
        self.label_date = Label(self, text='')
        self.label_date.grid(column=1, row=0, padx=15, pady=5)

        # Tlačítko pro náhled / preview
        # Volá parent callback, např. otevře popup s informacemi
        self.btn_preview = Button(self, text="🔎", command=self.email_preview)
        self.btn_preview.grid(column=2, row=0)

        self.btn_importance = SkullToggle(self,self.data)
        self.btn_importance.grid(column=3,row=0)

        # Tlačítko pro odstranění řádku
        # Volá callback parentu, který řádek smaže z listu a přepočítá grid
        self.btn_delete = Button(self, text="x", command=lambda: remove_callback(self))
        self.btn_delete.grid(column=4, row=0)

    def email_preview(self):
        """Debug preview (index řádku)"""
        self.EmailConstructor(self.config,self.data, self.importance_toggle).set_email_body()
        text = self.data.email_body
        converted_text = self.html_converter(text)

        popup = tk.Toplevel(self.parent)
        popup.wm_title("🔎")

        HTMLLabel(popup, html=converted_text,height=30,padx=25,pady=25).pack()

    def on_enter(self,event):
        self.parent.on_select(event)

    def on_down(self, event):
        if self.parent.dropdown:
            self.parent.dropdown.listbox.focus_set()
            self.parent.dropdown.listbox.selection_clear(0, "end")
            self.parent.dropdown.listbox.selection_set(0)
            self.parent.dropdown.listbox.activate(0)
        return "break"

    def safe_set_values(self, email, exp_date, exp_time):
        self.is_updating = True
        try:
            self.email = email
            self.exp_date = exp_date
            self.exp_time = exp_time

            self.entry_email.delete(0, tk.END)
            self.entry_email.insert(0, self.email)

            self.label_date.config(text=f"{exp_date} {exp_time}")
        finally:
            self.is_updating = False
    def set_data(self):
        self.data.email = self.email
        self.data.exp_date = self.exp_date
        self.data.exp_time = self.exp_time

        return self.data


class EmailDropDownMenu(tk.Toplevel):

    def __init__(self, root, row, parent):
        super().__init__(root)

        self.root = root
        self.row = row
        self.parent = parent

        # bez title baru
        self.wm_overrideredirect(True)

        # vždy nahoře
        self.attributes("-topmost", True)

        # pozice popupu
        self.update_position()

        # bindy
        self.root.bind("<Configure>", self._on_window_move, add="+")
        self.root.bind("<Unmap>", self._on_minimize, add="+")
        self.root.bind("<<NotebookTabChanged>>", self._on_tab_change, add="+")
        self.bind("<Return>", self.on_enter)
        self.root.bind("<Button-1>", self.on_click_outside)
    # =========================
    # POSITION
    # =========================
    def on_enter(self, event):
        if self.parent.dropdown:
            self.parent.on_select(event)

        return "break"
    def update_position(self):

        try:
            x = self.row.entry_email.winfo_rootx()

            y = (
                self.row.entry_email.winfo_rooty()
                + self.row.entry_email.winfo_height()
            )

            self.geometry(f"+{x}+{y}")

        except tk.TclError:
            pass

    def _on_window_move(self, event):
        self.update_position()

    # =========================
    # CLOSE EVENTS
    # =========================

    def _on_minimize(self, event):
        self.safe_destroy()

    def _on_tab_change(self, event):
        self.safe_destroy()

    def on_click_outside(self, event):

        try:
            widget = event.widget

            # klik uvnitř dropdownu
            if str(widget).startswith(str(self)):
                return

            # klik do entry
            if widget == self.row.entry_email:
                return

            self.safe_destroy()

        except tk.TclError:
            pass
    # =========================
    # DESTROY
    # =========================

    def safe_destroy(self):

        try:
            self.destroy()

        except tk.TclError:
            pass

class SkullToggle(tk.Button):
    """
        Vlastní Tkinter button fungující jako toggle přepínač.

        Button mění svůj vizuální stav po kliknutí:
        - vypnutý stav = šedé pozadí
        - zapnutý stav = žluté pozadí
        """
    def __init__(self, master,data, **kwargs):
        # inicializace základního Tkinter Button widgetu
        super().__init__(master, text="💀", width=4, **kwargs)

        self.data = data
        self.state = 1
        self.config(command=lambda: self.cycle(self.data))
        self.master = master


    def cycle(self,data):
        if self.state >= 3:
            self.state = 1
        else:
            self.state += 1
        self.update_style()
        self.set_state(data)


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
    def set_state(self,data):
        data.importance = self.state

@dataclass
class EmailData:
    exp_date: str
    exp_time: str
    email_body: str
    email: str
    importance:int