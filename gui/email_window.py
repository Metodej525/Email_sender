from tkinter import Frame, Button, Entry, Label




class EmailTab(Frame):

    def __init__(self,notebook):
        super().__init__(notebook)
        self.toolbox()
        self.default_row()
        self.rows = []


    def toolbox(self):
        Label(self,text='Email').grid(column=0,row=0)
        Label(self,text='Datum vypršení certifikátu').grid(column=1,row=0)
    def default_row(self):
        btn_add_email = Button(self,text='add',command=self.add_email)
        btn_add_email.grid(column=2,row=1)

        entry_email = Entry(self)
        entry_email.grid(column=0,row=1)

        entry_date = Entry(self)
        entry_date.grid(column=1,row=1)

    def add_email(self):
        row = EmailRow(self, self.remove_row, self.email_preview)

        self.rows.append(row)

        row.grid(row=len(self.rows), column=0, columnspan=4, sticky="w")

    def remove_row(self, row):

        row.destroy()

        self.rows.remove(row)

        for i, r in enumerate(self.rows):
            r.grid_configure(row=i + 1)

    def send_email(self):
        pass

    def reset_rows(self):
        self.default_row()
        for i in self.rows:
            for key,widget in i.items():
                widget.destroy()
        self.rows = []

    def email_preview(self):
        pass

class EmailRow(Frame):

    def __init__(self, parent, remove_callback, preview_callback):
        super().__init__(parent)

        self.entry_email = Entry(self)
        self.entry_email.grid(column=0, row=0)

        self.entry_date = Entry(self)
        self.entry_date.grid(column=1, row=0)

        btn_delete = Button(self, text="x", command=lambda: remove_callback(self))
        btn_delete.grid(column=2, row=0)

        btn_preview = Button(self, text="🔎", command=preview_callback)
        btn_preview.grid(column=3, row=0)