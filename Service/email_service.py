from datetime import timedelta, datetime
import constants as c
from utils import remove_diacritics
import tkinter as tk
from email_validator import validate_email, EmailNotValidError

def get_emails(rows):
    """gets email addresses from entries """
    emails = []
    for row in rows:
        widgets = row.winfo_children()
        for widget in widgets:
            if isinstance(widget, tk.Entry):
                email = widget.get()
                emails.append(email)
    return emails

def check_email(email):
    """checks if email format is ok"""
    email_info = validate_email(email, check_deliverability=True)
    return email_info.normalized

def email_sender(rows):
    """sends email/s"""
    emails = get_emails(rows)
    for email in emails:
        normalized_email = check_email(email)
        print(normalized_email)



def load_email_details(config):
    smtp_server = config.get(c.EMAIL_SECTION, c.EMAIL_SMTP_SERVER, fallback='')
    smtp_port = config.get(c.EMAIL_SECTION, c.EMAIL_SMTP_PORT, fallback='')
    username = config.get(c.EMAIL_SECTION, c.EMAIL_USERNAME, fallback='')
    sender_email = config.get(c.EMAIL_SECTION, c.EMAIL_SENDER, fallback='')
    subject = config.get(c.EMAIL_SECTION, c.EMAIL_SUBJECT, fallback='')
    body1 = config.get(c.EMAIL_SECTION, c.EMAIL_BODY_1, fallback='')
    body2 = config.get(c.EMAIL_SECTION, c.EMAIL_BODY_2, fallback='')
    body3 = config.get(c.EMAIL_SECTION, c.EMAIL_BODY_3, fallback='')
    sign = config.get(c.EMAIL_SECTION, c.EMAIL_SIGN, fallback='')


    return {'smtp_server': smtp_server,
            'smtp_port': smtp_port,
            'username': username,
            'sender_email': sender_email,
            'subject': subject,
            'body': f'{body1} datum {body2} datum {body3} {sign}'
            }
def specific_email_preview(config,exp_date,exp_time):
    body1 = config.get(c.EMAIL_SECTION, c.EMAIL_BODY_1, fallback='')
    body2 = config.get(c.EMAIL_SECTION, c.EMAIL_BODY_2, fallback='')
    body3 = config.get(c.EMAIL_SECTION, c.EMAIL_BODY_3, fallback='')
    sign =  config.get(c.EMAIL_SECTION, c.EMAIL_SIGN, fallback='')
    minus_exp_date = minus_day_counter(exp_date)


    body = f'{body1} {exp_date} {exp_time} {body2} {minus_exp_date} {body3} {sign}'
    return body
def selected_value_manager(value):
    raw_surname, raw_firstname, login, cert_type, exp = [x.strip() for x in value.split(',')]
    exp_date, exp_time = exp.split()
    surname = remove_diacritics(raw_surname.lower())
    firstname = remove_diacritics(raw_firstname.lower())

    email = f"{firstname}.{surname}@ikem.cz"
    print(email,exp_date, exp_time)
    return email, exp_date, exp_time
def html_converter(html_text):
    """Raw html body to plain text"""
    html = html_text.replace('\r\n\r\n', '</p><p>')
    html = html.replace('\n\n', '</p><p>')

    # Převod jednotlivých nových řádků na <br>
    html = html.replace('\r\n', '<br>')
    html = html.replace('\n', '<br>')

    # Obal pro celý text do <p>
    html = f"<p>{html}</p>"
    return html
def minus_day_counter(exp_date:str):
    t = datetime.strptime(exp_date, "%d.%m.%Y")
    raw_date = t - timedelta(days=1)
    raw_date = raw_date.strftime('%d.%m')
    return raw_date


