from tkinter import Frame, Button, Entry, Label, StringVar, Listbox
import tkinter as tk
import tkinter.messagebox

class EmailTab(Frame):
    def __init__(self, notebook, root, excel_search, config, df,selected_value_manager):
        super().__init__(notebook)

        # --- state ---
        self.rows = []                         # list of EmailRow instances
        self.root = root                       # reference na root (kvůli Toplevel, bindům)
        self.config = config
        self.excel_search = excel_search       # callback pro live search
        self.df = df
        self.btn_send_email = None
        self.selected_value_manager = selected_value_manager

        # --- global event bindings ---
        # reposition dropdown při pohybu okna
        self.root.bind("<Configure>", self._on_window_move)

        # zavření dropdownu při změně tabu
        self.root.bind("<<NotebookTabChanged>>", self._on_notebook_change)

        # zavření dropdownu při minimalizaci
        self.root.bind("<Unmap>", self._on_minimize)

        self.toolbox()
        self.default_row()

    def toolbox(self):
        """Header labels"""
        Label(self, text='Email').grid(column=0, row=0, pady=5, padx=5)
        Label(self, text='Datum vypršení certifikátu').grid(column=1, row=0, pady=5, padx=5)

    def default_row(self):
        """Inicializuje první (defaultní) řádek"""
        row = EmailRow(self, self.remove_row, self.email_preview)
        row.grid(row=len(self.rows) + 1, column=0, columnspan=5, sticky="w")

        self.rows.append(row)

        # první řádek nemá delete tlačítko
        for widget in self.rows[0].winfo_children():
            if isinstance(widget, Button) and widget.cget("text") == "x":
                widget.destroy()

        # reset send buttonu
        if self.btn_send_email:
            self.btn_send_email.destroy()

        self.create_send_btn(2)

    def add_email(self):
        """Přidá nový emailový řádek (max 5)"""
        if self.btn_send_email:
            self.btn_send_email.destroy()
            self.create_send_btn(len(self.rows) + 3)

        if len(self.rows) < 5:
            row = EmailRow(self, self.remove_row, self.email_preview)
            self.rows.append(row)
            row.grid(row=len(self.rows) + 1, column=0, columnspan=5, sticky="w")

    def create_send_btn(self, row):
        """Vytvoří tlačítko pro odeslání"""
        self.btn_send_email = Button(self, text='Odeslat email', command=self.send_email)
        self.btn_send_email.grid(column=1, row=row)

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

    def send_email(self):
        """Potvrzení a odeslání emailu"""
        if tkinter.messagebox.askquestion(title='', message='Odeslat email?') == 'yes':
            self._pop_up_window('', 'Email byl odeslán')
            self.reset_rows()

    def reset_rows(self):
        """Reset UI do výchozího stavu"""
        for tab in self.rows:
            tab.destroy()

        self.rows.clear()
        self.default_row()

    def email_preview(self, row):
        """Debug preview (index řádku)"""
        if row in self.rows:
            label_text = str(self.rows.index(row))
        else:
            label_text = '-1'

        popup = tk.Toplevel(self.root)
        popup.wm_title("🔎")
        tk.Label(popup, text=label_text).pack()

    def on_search_change(self, row):
        """Trigger live search (debounced z EmailRow)"""
        if row in self.rows:
            email_val = str(row.entry_email.get())
            if len(email_val) >= 3:
                self.live_search(email_val, row)

    # =========================
    # DROPDOWN MANAGEMENT
    # =========================

    def _on_notebook_change(self, event):
        """Zavře dropdown při změně tabu"""
        self._close_dropdown()

    def _on_minimize(self, event):
        """Zavře dropdown při minimalizaci"""
        self._close_dropdown()

    def _close_dropdown(self):
        """Bezpečné zavření dropdownu"""
        if hasattr(self, "dropdown") and self.dropdown:
            try:
                self.dropdown.destroy()
            except:
                pass

            self.dropdown = None
            self.active_row = None

    def _on_window_move(self, event):
        """Reposition dropdownu při pohybu okna"""
        if hasattr(self, "dropdown") and self.dropdown and hasattr(self, "active_row"):
            row = self.active_row
            try:
                x = row.entry_email.winfo_rootx()
                y = row.entry_email.winfo_rooty() + row.entry_email.winfo_height()
                self.dropdown.geometry(f"+{x}+{y}")
            except:
                # row mohl být mezitím zničen
                pass

    def _on_click_outside(self, event):
        """Zavře dropdown při kliknutí mimo"""
        if not hasattr(self, "dropdown") or not self.dropdown:
            return

        widget = event.widget

        # klik uvnitř dropdownu → ignoruj
        if str(widget).startswith(str(self.dropdown)):
            return

        # klik do aktivního entry → ignoruj
        if hasattr(self, "active_row") and widget == self.active_row.entry_email:
            return

        self._close_dropdown()

    def live_search(self, email_val, row):
        """Vykreslí autocomplete dropdown"""
        values = self.excel_search(email_val, self.df)

        self.root.bind("<Button-1>", self._on_click_outside)
        self.active_row = row

        # transformace dat do stringu
        stripped_values_list = [
            ', '.join(map(str, row_data)) for row_data in values
        ]

        # zrušení starého dropdownu
        if hasattr(self, "dropdown") and self.dropdown:
            self.dropdown.destroy()

        # vytvoření nového dropdownu
        self.dropdown = tk.Toplevel(self.root)
        self.dropdown.wm_overrideredirect(True)

        # pozice pod Entry
        x = row.entry_email.winfo_rootx()
        y = row.entry_email.winfo_rooty() + row.entry_email.winfo_height()
        self.dropdown.geometry(f"+{x}+{y}")

        lb = Listbox(self.dropdown, width=80, height=min(5, len(values)))
        lb.pack()

        for val in stripped_values_list[:5]:
            lb.insert(tk.END, val)

        lb.bind('<Double-Button-1>', self.on_select)

    def on_select(self, event):
        """Výběr hodnoty z dropdownu"""
        lb = event.widget
        selection = lb.curselection()

        if selection:
            value = lb.get(selection[0])
            self._close_dropdown()
            self.add_email()
            print(value)
            self.selected_value_manager(value)


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

    def __init__(self, parent, remove_callback, preview_callback):
        super().__init__(parent)

        # --- internal state ---
        self._after_id = None               # uchovává ID 'after' pro debounce
        self.search_email_var = StringVar() # propojení Entry ↔ live search

        # ------------------------------
        # Debounce callback pro live search
        # ------------------------------
        def trace_callback(*args):
            """
            Triggerováno při každé změně Entry.
            Debounce – pokud už byl naplánován after, zruší ho a naplánuje nový.
            """
            if self._after_id:
                self.after_cancel(self._after_id)
            # zavolá parent.on_search_change po 200 ms, pokud uživatel nepíše dál
            self._after_id = self.after(200, lambda: parent.on_search_change(self))

        # připojení callbacku na změnu StringVar
        self.search_email_var.trace_add("write", trace_callback)

        # ------------------------------
        # UI komponenty
        # ------------------------------

        # Entry pro email
        self.entry_email = Entry(self, textvariable=self.search_email_var)
        self.entry_email.grid(column=0, row=0, padx=5, pady=5)

        # Label – placeholder
        Label(self, text='hehe').grid(column=1, row=0, padx=15, pady=5)

        # Tlačítko pro odstranění řádku
        # Volá callback parentu, který řádek smaže z listu a přepočítá grid
        btn_delete = Button(self, text="x", command=lambda: remove_callback(self))
        btn_delete.grid(column=2, row=0)

        # Tlačítko pro náhled / preview
        # Volá parent callback, např. otevře popup s informacemi
        btn_preview = Button(self, text="🔎", command=lambda: preview_callback(self))
        btn_preview.grid(column=3, row=0)