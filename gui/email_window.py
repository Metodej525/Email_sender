from tkinter import Frame, Button

class EmailTab(Frame):
    def __init__(self,notebook, add_email_receiver):
        super().__init__(notebook)
        self.add_email_receiver = add_email_receiver
        notebook.add(self, text='Email')
        Button(self, text='přidej email', command=add_email_receiver).grid(column=2,row=0)