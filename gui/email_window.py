from tkinter import Frame, Button, Entry, Label
import tkinter as tk

class EmailTab(Frame):

    def __init__(self,notebook,root):
        super().__init__(notebook)
        self.toolbox()
        self.default_row()
        self.rows = []
        self.root = root
        self.btn_send_email_list = []
        self.btn_send_email = None

    def toolbox(self):
        Label(self,text='Email').grid(column=0,row=0,pady=5,padx=5)
        Label(self,text='Datum vypršení certifikátu').grid(column=1,row=0,pady=5,padx=5)
    def default_row(self):
        btn_add_email = Button(self,text='add',command=self.add_email)
        btn_add_email.grid(column=2,row=1)

        entry_email = Entry(self)
        entry_email.grid(column=0,row=1,pady=5,padx=5)

        entry_date = Entry(self)
        entry_date.grid(column=1,row=1,pady=5,padx=5)

        btn_preview = Button(self, text="🔎", command=lambda: self.email_preview(self))
        btn_preview.grid(column=3, row=1)

        self.btn_send_email = Button(self, text='Odeslat email', command='')
        self.btn_send_email.grid(column=2, row=1)

        self.btn_send_email_list.append(btn_add_email)

    def add_email(self):
        if self.btn_send_email in self.btn_send_email_list:
            self.btn_send_email_list.clear()
            self.btn_send_email.destroy()
            if len(self.rows) < 4:
                row = EmailRow(self, self.remove_row, self.email_preview)

                self.rows.append(row)

                row.grid(row=len(self.rows)
                         +1, column=0, columnspan=5, sticky="w")


    def remove_row(self, row):

        row.destroy()

        self.rows.remove(row)

        for i, r in enumerate(self.rows):
            r.grid_configure(row=i + 2)
            print(i)

    def send_email(self):
        pass

    def reset_rows(self):
        self.default_row()
        for i in self.rows:
            for key,widget in i.items():
                widget.destroy()
        self.rows = []

    def email_preview(self,row):
        if row in self.rows:
            index = str(self.rows.index(row))
            label_text = ''.join(index)
        else:
            label_text = '-1'

        email_preview_popup = tk.Toplevel(self.root)
        email_preview_popup.wm_title("🔎")
        tk.Label(email_preview_popup, text=label_text).pack()

    def live_search(self):
        pass

class EmailRow(Frame):

    def __init__(self, parent, remove_callback, preview_callback):
        super().__init__(parent)

        self.entry_email = Entry(self)
        self.entry_email.grid(column=0, row=0,padx=5,pady=5)

        self.entry_date = Entry(self)
        self.entry_date.grid(column=1, row=0,padx=15,pady=5)

        btn_delete = Button(self, text="x", command=lambda: remove_callback(self))
        btn_delete.grid(column=2, row=0)

        btn_preview = Button(self, text="🔎", command=lambda: preview_callback(self))
        btn_preview.grid(column=3, row=0)

