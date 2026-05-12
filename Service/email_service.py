from datetime import timedelta, datetime
import constants as c
from utils import remove_diacritics
import tkinter as tk
from email_validator import validate_email, EmailNotValidError
from Service.email_details import email_details

def get_emails(rows):
    """gets email addresses from entries """
    email_dict = {}
    for row in rows:
        row_dict = row.row_to_dict()
        email_dict[row_dict['email']] = row_dict['email_body']

    return email_dict

def check_email(rows):
    """checks if email format is ok"""
    checked_dict = {}
    email_dict = get_emails(rows)
    for email,body in email_dict.items():
        try:
            email_info = validate_email(email, check_deliverability=True)
            email = email_info.normalized
            checked_dict[email] = body
        except EmailNotValidError:
            raise

    return checked_dict

def email_sender(config,rows):
    """sends email/s"""
    checked_dict = check_email(rows)
    for email, body in checked_dict.items():
        email_details(config,email,body)

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
    minus_exp_date = previous_workday(exp_date)


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
def previous_workday(exp_date: str):
    t = datetime.strptime(exp_date, "%d.%m.%Y")

    while True:
        t -= timedelta(days=1)

        # 0-4 = Po-Pá
        if t.weekday() < 5:
            return t.strftime("%d.%m")


