import constants as c
from utils import remove_diacritics

def send_email():
    # #po 2 sekundách label skryje, pro kazdy label bezi samostatny timeout jestli nekdo bude klikat jak jeblej tak se to rozbije
    pass


def load_email_details(config):
    smtp_server = config.get(c.EMAIL_SECTION, c.EMAIL_SMTP_SERVER, fallback='')
    smtp_port = config.get(c.EMAIL_SECTION, c.EMAIL_SMTP_PORT, fallback='')
    username = config.get(c.EMAIL_SECTION, c.EMAIL_USERNAME, fallback='')
    sender_email = config.get(c.EMAIL_SECTION, c.EMAIL_SENDER, fallback='')
    subject = config.get(c.EMAIL_SECTION, c.EMAIL_SUBJECT, fallback='')
    body = config.get(c.EMAIL_SECTION, c.EMAIL_BODY, fallback='')
    return {'smtp_server': smtp_server,
            'smtp_port': smtp_port,
            'username': username,
            'sender_email': sender_email,
            'subject': subject,
            'body': body
            }

def selected_value_manager(value):
    raw_surname, raw_firstname, login, cert_type, exp = [x.strip() for x in value.split(',')]
    exp_date, exp_time = exp.split()

    # fields = {
    #     'surname': raw_surname,
    #     'firstname': raw_firstname,
    #     'login': login,
    #     'cert_type': cert_type,
    #     'exp_date': exp_date,
    #     'exp_time': exp_time
    # }
    surname = remove_diacritics(raw_surname.lower())
    firstname = remove_diacritics(raw_firstname.lower())

    email = f"{firstname}.{surname}@ikem.cz"
    print(email,exp_date, exp_time)
    return email, exp_date, exp_time
