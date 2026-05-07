from tkinter import Label, Frame
from tkhtmlview import HTMLLabel

class EmailPreviewTab(Frame):
    """
        Tkinter tab for email preview.

        Loads values from config and automatically replaces them.
        """
    FIELDS = {'from':('Od: ','sender_email'),
              'to':('Komu: ','receiver_email'),
              'subject':('Předmět: ','subject'),
              'preview':('Náhled: ','')
              }

    def __init__(self,notebook,load_email_details,html_converter,config):
        super().__init__(notebook)
        self.load_email_details = load_email_details(config)
        self.html_converter = html_converter

        for row, (key, (label_text, config_text)) in enumerate(self.FIELDS.items()):
            Label(self,text=label_text).grid(column=0,row=row,sticky="nw",padx=5,pady=5)
            config_value = config.get('EMAIL', config_text, fallback='')
            Label(self,text=config_value).grid(column=1,row=row,sticky="nw",padx=5,pady=5)

        html = self.html_converter(self.load_email_details['body'])


        email_label = HTMLLabel(self, html=html,height=100)
        email_label.grid(column=1, row=3, padx=25, pady=0)