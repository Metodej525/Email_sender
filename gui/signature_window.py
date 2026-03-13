from tkinter import Button, Entry, Label, Frame

class SignatureTab(Frame):
    def __init__(self, notebook,config,save_signature,safe_write_config,load_signature_data):
        super().__init__(notebook)
        self.config = config
        self.save_signature=save_signature
        self.safe_write_config= safe_write_config
        self.signature_data= load_signature_data(self.config)
        self.load_signature_data = load_signature_data

        #label + entry na jméno a příjmení
        Label(self, text='Jméno a přijmení: ').grid(column=0,row=0)
        self.name_entry = Entry(self)
        self.name_entry.grid(column=1,row=0)

        #label + entry na tel. číslo
        Label(self, text='Tel. číslo: ').grid(column=0,row=1)
        self.telephone_entry = Entry(self)
        self.telephone_entry.grid(column=1,row=1)

        #label + entry na pozici pracovníka
        Label(self, text='Pracovní pozice').grid(column=0,row=2)
        self.position_entry = Entry(self)
        self.position_entry.grid(column=1,row=2)
        #label + entry na organizační členění
        Label(self, text='Org. členění').grid(column=0,row=3)
        self.department_entry = Entry(self)
        self.department_entry.grid(column=1,row=3)
        #label + entry na login
        Label(self, text='Login').grid(column=0,row=4)
        self.login_entry = Entry(self)
        self.login_entry.grid(column=1,row=4)
        #label + entry na email
        Label(self, text='Email').grid(column=0, row=5)
        self.email_entry = Entry(self)
        self.email_entry.grid(column=1, row=5)
        #button na uložení podpisu
        Button(self, text='uložit podpis',command=self.on_save).grid(column=1,row=6)
        self.default_entry_data()

    #funkce pro button ulozit podpis, ulozi data do slovniku a zavola funkci pro ulozeni do configu + temp_label pro info
    #ze s email ulozil
    def on_save(self):
        data = {
            "name": self.name_entry.get(),
            "telephone": self.telephone_entry.get(),
            "department": self.department_entry.get(),
            "position": self.position_entry.get(),
            'login': self.login_entry.get(),
            'email':self.email_entry.get()
        }

        self.save_signature(self.config, data, self.safe_write_config)
        self.signature_data = self.load_signature_data(self.config)

        temp_label = Label(self, text='podpis uložen')
        temp_label.grid(column=0, row=7, columnspan=2)
        self.after(2000, temp_label.destroy)

    #nacte defualt data z konfigu a insertne do entry, aby uzivatel vedel co tam je
    def default_entry_data(self):
        self.name_entry.insert(0, self.signature_data['name'])
        self.telephone_entry.insert(0, self.signature_data['telephone'])
        self.position_entry.insert(0, self.signature_data['position'])
        self.department_entry.insert(0, self.signature_data['department'])
        self.login_entry.insert(0, self.signature_data['login'])
        self.email_entry.insert(0,self.signature_data['email'])