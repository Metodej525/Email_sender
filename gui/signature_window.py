from tkinter import Button, Entry, Label, Frame, messagebox

class SignatureTab(Frame):
    FIELDS = [
        ("name", "Jméno a přijmení:"),
        ("telephone", "Tel. číslo:"),
        ("position", "Pracovní pozice:"),
        ("department", "Org. členění:"),
        ("login", "Login:"),
        ("email", "Email:")
    ]

    def __init__(self, notebook,config,save_signature,safe_write_config,load_signature_data):
        super().__init__(notebook)
        self.config = config
        self.save_signature=save_signature
        self.safe_write_config= safe_write_config
        self.signature_data = load_signature_data(self.config)
        self.load_signature_data = load_signature_data

        self.dict_entries = {}

        for n,(key,label_text) in enumerate(self.FIELDS):
            Label(self, text=label_text).grid(column=0, row=n)
            entry = Entry(self)
            entry.grid(column=1,row=n)
            entry.insert(0,self.signature_data[key])
            self.dict_entries[key]=entry

        Button(self, text='uložit podpis',command=self.on_save).grid(column=1,row=6)


    #funkce pro button ulozit podpis, ulozi data do slovniku a zavola funkci pro ulozeni do configu + temp_label pro info
    #ze s email ulozil
    def on_save(self):
        data = {}
        for key,entry in self.dict_entries.items():
            data[key] = entry.get()
        self.save_signature(self.config, data, self.safe_write_config)
        self.signature_data = self.load_signature_data(self.config)
        self._pop_up_window('','podpis uložen')
    @staticmethod
    def _pop_up_window(title, text):
        messagebox.showinfo(title=title, message=text)
