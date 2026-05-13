from os import remove
from tkinter import Frame, Button, Entry, Label, StringVar, Listbox
import tkinter as tk
import tkinter.messagebox
from tkhtmlview import HTMLLabel



class EmailTab(Frame):
    def __init__(self, notebook, root, excel_search, config, df,selected_value_manager,html_converter,email_sender,specific_email_preview):
        super().__init__(notebook)

        # --- state ---
        self.rows = []                         # list of EmailRow instances
        self.root = root                       # reference na root (kvůli Toplevel, bindům)
        self.config = config
        self.excel_search = excel_search       # callback pro live search
        self.df = df
        self.btn_send_email = None
        self.selected_value_manager = selected_value_manager
        self.specific_email_preview = specific_email_preview
        self.html_converter = html_converter
        self.email_sender = email_sender
        self.dropdown = None
        self.toolbox()
        self.default_row()

    def toolbox(self):
        """Header labels"""
        Label(self, text='Email').grid(column=0, row=0, pady=5, padx=25)
        # Label(self, text='Datum vypršení certifikátu').grid(column=1, row=0, pady=5, padx=75)

    def default_row(self):
        """Inicializuje první (defaultní) řádek"""
        row = EmailRow(self, self.config, self.remove_row, self.email_preview,self.specific_email_preview)
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
        if self.btn_send_email:
            self.btn_send_email.destroy()
            self.create_send_btn(len(self.rows) + 3)

        if len(self.rows) < 5:
            row = EmailRow(self,self.config, self.remove_row, self.email_preview,self.specific_email_preview)
            self.rows.append(row)
            row.grid(row=len(self.rows) + 1, column=0, columnspan=5, sticky="w")
        self.check_add_email_btn_grid()

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
            self.email_sender(self.config,self.rows)
            self.reset_rows()

    def reset_rows(self):
        """Reset UI do výchozího stavu"""
        for row in self.rows:
            row.destroy()

        self.rows.clear()
        self.default_row()

    def email_preview(self, row):
        """Debug preview (index řádku)"""
        text = row.email_body
        converted_text = self.html_converter(text)

        if row in self.rows:
            label_text = converted_text
        else:
            label_text = ':('

        popup = tk.Toplevel(self.root)
        popup.wm_title("🔎")
        HTMLLabel(popup, html=label_text,height=30,padx=25,pady=25).pack()
        # self.exp_time = []
        # self.exp_date = []

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
        self.dropdown = EmailDropDownMenu(self.root, row)

        # Listbox
        lb = Listbox(
            self.dropdown,
            width=50,
            height=min(5, len(stripped_values_list))
        )
        lb.pack(fill="both", expand=True)

        # vložení hodnot
        for val in stripped_values_list[:5]:
            lb.insert(tk.END, val)

        # select event
        lb.bind(
            "<Double-Button-1>",
            lambda event: self.on_select(event)
        )

        # click outside
        self.root.bind(
            "<Button-1>",
            self.dropdown.on_click_outside,
            add="+"
        )

    def on_select(self, event):
        lb = event.widget
        selection = lb.curselection()

        if selection:
            value = lb.get(selection[0])

            row = self.active_row
            if self.rows.index(self.active_row) == len(self.rows) -1:
                self.add_email()
            self.dropdown.safe_destroy()

            email, exp_date, exp_time = self.selected_value_manager(value)

            row.safe_set_values(email, exp_date, exp_time)

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

    def __init__(self, parent, config, remove_callback, preview_callback, specific_email_preview):
        super().__init__(parent)

        # --- internal state ---
        self._after_id = None               # uchovává ID 'after' pro debounce
        self.is_updating = False  # flag pro regulaci trace_callback
        self.search_email_var = StringVar() # propojení Entry ↔ live search
        self.exp_date = None
        self.exp_time = None
        self.email_body = None
        self.email = None
        self.config = config
        self.specific_email_preview = specific_email_preview

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

        # Label – placeholder
        self.label_date = Label(self, text='')
        self.label_date.grid(column=1, row=0, padx=15, pady=5)

        # Tlačítko pro náhled / preview
        # Volá parent callback, např. otevře popup s informacemi
        self.btn_preview = Button(self, text="🔎", command=lambda: preview_callback(self))
        self.btn_preview.grid(column=2, row=0)

        self.btn_importance = SkullToggle(self)
        self.btn_importance.grid(column=3,row=0)

        # Tlačítko pro odstranění řádku
        # Volá callback parentu, který řádek smaže z listu a přepočítá grid
        self.btn_delete = Button(self, text="x", command=lambda: remove_callback(self))
        self.btn_delete.grid(column=4, row=0)

    def safe_set_values(self, email, exp_date, exp_time):
        self.is_updating = True
        try:
            self.email = email
            self.exp_date = exp_date
            self.exp_time = exp_time
            self.email_body = self.specific_email_preview(self.config, self.exp_date, self.exp_time)
            self.entry_email.delete(0, tk.END)
            self.entry_email.insert(0, self.email)

            self.label_date.config(text=f"{exp_date} {exp_time}")


        finally:
            self.is_updating = False
    def row_to_dict(self):
        row_dict = {'exp_date': self.exp_date,
                    'exp_time': self.exp_time,
                    'email_body': self.email_body,
                    'email': self.email}
        return row_dict
    def importance_toggle(self):
        pass

class EmailDropDownMenu(tk.Toplevel):

    def __init__(self, root, row):
        super().__init__(root)

        self.root = root
        self.row = row

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

    # =========================
    # POSITION
    # =========================

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
    def __init__(self, master, **kwargs):
        super().__init__(master, text="💀", width=4, **kwargs)

        self.state = False
        self.config(command=self.toggle)

        self.update_style()

    def toggle(self):
        self.state = not self.state
        self.update_style()

    def update_style(self):
        if self.state:
            self.config(
                text="💀",
                bg="#fff176",
                activebackground="#fff59d",
                relief="sunken"
            )
        else:
            self.config(
                text="💀",
                bg="#e0e0e0",
                activebackground="#eeeeee",
                relief="raised"
            )