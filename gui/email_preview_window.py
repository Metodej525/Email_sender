from tkinter import Label, Frame
from tkhtmlview import HTMLLabel

class EmailPreviewTab(Frame):
    """
        Tkinter tab for email preview.

        Loads values from config and automatically replaces them.
        """
    FEILDS = {'from':('Od: ','sender_email'),
              'to':('Komu: ','receiver_email'),
              'subject':('Předmět: ','subject'),
              'preview':('Náhled: ','')
              }

    def __init__(self,notebook,load_email_details,config):
        super().__init__(notebook)
        self.load_email_details = load_email_details(config)
        for row, (key, (label_text, config_text)) in enumerate(self.FEILDS.items()):
            Label(self,text=label_text).grid(column=0,row=row,sticky="nw",padx=5,pady=5)
            config_value = config.get('EMAIL', config_text, fallback='')
            Label(self,text=config_value).grid(column=1,row=row,sticky="nw",padx=5,pady=5)
        html = self.load_email_details['body'].encode('cp1250').decode('utf-8', errors='ignore')
        # Převod dvojitých novinek na odstavce
        html = html.replace('\r\n\r\n', '</p><p>')
        html = html.replace('\n\n', '</p><p>')

        # Převod jednotlivých nových řádků na <br>
        html = html.replace('\r\n', '<br>')
        html = html.replace('\n', '<br>')

        # Obal pro celý text do <p>
        html = f"<p>{html}</p>"
        email_label = HTMLLabel(self, html=html)
        email_label.grid(column=1, row=3, padx=25, pady=0)