from os.path import exists
from tkinter import Frame, Button, Entry, Label
import tkinter as tk
import tkinter.messagebox

class EmailTab(Frame):
    def __init__(self,notebook,root):
        super().__init__(notebook)
        self.rows = []
        self.root = root

        self.btn_send_email = None
        self.toolbox()
        self.default_row()

    def toolbox(self):
        Label(self,text='Email').grid(column=0,row=0,pady=5,padx=5)
        Label(self,text='Datum vypršení certifikátu').grid(column=1,row=0,pady=5,padx=5)

    def default_row(self):
        btn_add_email = Button(self,text='add',command=self.add_email)
        btn_add_email.grid(column=5,row=1,sticky="w")

        row = EmailRow(self, self.remove_row, self.email_preview)
        row.grid(row=len(self.rows)
                     + 1, column=0, columnspan=5, sticky="w")
        self.rows.append(row)
        for widget in self.rows[0].winfo_children():
            if isinstance(widget, Button) and widget.cget("text") == "x":
                widget.destroy()
        if self.btn_send_email:
            self.btn_send_email.destroy()

        self.create_send_btn(2)

    def add_email(self):
        if self.btn_send_email:
            self.btn_send_email.destroy()
            self.create_send_btn(len(self.rows)+3)

        if len(self.rows) < 5:
            row = EmailRow(self, self.remove_row, self.email_preview)

            self.rows.append(row)

            row.grid(row=len(self.rows)
                     +1, column=0, columnspan=5, sticky="w")

    def create_send_btn(self,row):
        self.btn_send_email = Button(self, text='Odeslat email', command=self.send_email)
        self.btn_send_email.grid(column=1, row=row)

    def remove_row(self, row):
        row.destroy()
        self.rows.remove(row)
        for i, r in enumerate(self.rows):
            r.grid_configure(row=i + 1)
            print(i)
        if self.btn_send_email:
            self.btn_send_email.destroy()
        self.create_send_btn(len(self.rows) + 1)

    def send_email(self):
        if tkinter.messagebox.askquestion(title='',message='Odeslat email?') == 'yes':
            self.pop_up_window('','Email byl odeslán')
            self.reset_rows()

    def reset_rows(self):
        for tab in self.rows:
            tab.destroy()

        self.rows.clear()
        self.default_row()

    def email_preview(self,row):
        if row in self.rows:
            index = str(self.rows.index(row))
            label_text = ''.join(index)
        else:
            label_text = '-1'
        email_preview_popup = tk.Toplevel(self.root)
        email_preview_popup.wm_title("🔎")
        tk.Label(email_preview_popup, text=label_text).pack()

    def live_search(self,excel_search,excel_load):
        pass
    @staticmethod
    def pop_up_window(title,text):
        tkinter.messagebox.showinfo(title=title,message=text)

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