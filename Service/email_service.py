import constants as c


def send_email():
    # #po 2 sekundách label skryje, pro kazdy label bezi samostatny timeout jestli nekdo bude klikat jak jeblej tak se to rozbije
    pass


def load_email_details(config):
    smtp_server = config.get(c.EXCEL_SECTION, c.EMAIL_SMTP_SERVER, fallback='')
    smtp_port = config.get(c.EXCEL_SECTION, c.EMAIL_SMTP_PORT, fallback='')
    username = config.get(c.EXCEL_SECTION, c.EMAIL_USERNAME, fallback='')
    sender_email = config.get(c.EXCEL_SECTION, c.EMAIL_SENDER, fallback='')
    subject = config.get(c.EXCEL_SECTION, c.EMAIL_SUBJECT, fallback='')
    body = config.get(c.EXCEL_SECTION, c.EMAIL_BODY, fallback='')
    return {'smtp_server': smtp_server,
            'smtp_port': smtp_port,
            'username': username,
            'sender_email': sender_email,
            'subject': subject,
            'body': body
            }

