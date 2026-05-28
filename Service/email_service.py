from datetime import timedelta, datetime
import constants as c
from core.utilities import remove_diacritics
from email_validator import validate_email, EmailNotValidError
from infra.email_details import email_details

import logging

logger = logging.getLogger(__name__)

def email_sender(config,data):
    """sends email/s"""
    email_none_state(data)
    validate_emails(data)

    for email_row in data:
        email_body = set_email_body(config,email_row)
        email_body = importance_toggle(email_body,email_row.importance)
        email_details(config, email_row.valid_email, email_body)
        logger.info(f"send email to: {email_row.valid_email}")

def email_none_state(data):
    """checks and deletes None values from dict"""
    logger.debug('checked for none state in email dict')
    for email_row in data:
        if email_row.email is None:
            email_row.remove()
def validate_emails(data):
    for email_row in data:
        try:
            email_info = validate_email(str(email_row.email), check_deliverability=True)
            email_row.valid_email = email_info.normalized
        except EmailNotValidError as e:
            logger.warning(f'email valid error: {e}')
            continue
def set_email_body(config,email_row):
    """loads preview of email in specific row and returns it"""
    body1 = config.get(c.EMAIL_SECTION, c.EMAIL_BODY_1, fallback='')
    body2 = config.get(c.EMAIL_SECTION, c.EMAIL_BODY_2, fallback='')
    body3 = config.get(c.EMAIL_SECTION, c.EMAIL_BODY_3, fallback='')
    sign =  config.get(c.EMAIL_SECTION, c.EMAIL_SIGN, fallback='')
    minus_exp_date = previous_workday(email_row.exp_date)
    email_body = f'{body1} {email_row.exp_date} {email_row.exp_time} {body2} {minus_exp_date} {body3} {sign}'
    return email_body
def load_email_details(config):
    """loads all email props and returns them as dict"""
    smtp_server = config.get(c.EMAIL_SECTION, c.EMAIL_SMTP_SERVER, fallback='')
    smtp_port = config.get(c.EMAIL_SECTION, c.EMAIL_SMTP_PORT, fallback='')
    username = config.get(c.EMAIL_SECTION, c.EMAIL_USERNAME, fallback='')
    sender_email = config.get(c.EMAIL_SECTION, c.EMAIL_SENDER, fallback='')
    subject = config.get(c.EMAIL_SECTION, c.EMAIL_SUBJECT, fallback='')
    body1 = config.get(c.EMAIL_SECTION, c.EMAIL_BODY_1, fallback='')
    body2 = config.get(c.EMAIL_SECTION, c.EMAIL_BODY_2, fallback='')
    body3 = config.get(c.EMAIL_SECTION, c.EMAIL_BODY_3, fallback='')
    sign = config.get(c.EMAIL_SECTION, c.EMAIL_SIGN, fallback='')

    logger.debug("default email details from config loaded")
    return {'smtp_server': smtp_server,
            'smtp_port': smtp_port,
            'username': username,
            'sender_email': sender_email,
            'subject': subject,
            'body': f'{body1} datum {body2} datum {body3} {sign}'
            }

def selected_value_manager(value):
    """loads on_select values and props them + makes email str"""
    raw_surname, raw_firstname, login, cert_type, exp = [x.strip() for x in value.split(',')]
    exp_date, exp_time = exp.split()
    surname = remove_diacritics(raw_surname.lower())
    firstname = remove_diacritics(raw_firstname.lower())
    logger.debug("diacritics removed")
    email = f"{firstname}.{surname}@ikem.cz"
    logger.debug(f'email set as: {email}, exp_date as: {exp_date}, exp_time as: {exp_time}')
    return email, exp_date, exp_time
def html_converter(html_text):
    """Raw HTML body to plain text, used in preview tab"""
    html = html_text.replace('\r\n\r\n', '</p><p>')
    html = html.replace('\n\n', '</p><p>')

    # Převod jednotlivých nových řádků na <br>
    html = html.replace('\r\n', '<br>')
    html = html.replace('\n', '<br>')

    # Obal pro celý text do <p>
    html = f"<p>{html}</p>"
    return html

def importance_toggle(email_body,importance_value):
    """Gives HTML text expect signature yellow background color"""
    importance = 'nizka'
    if importance_value == 2:
        importance = 'stredni'
        email_body = email_body.replace("<div>",
                            "<div>Dobrý den,<br/>připomínám níže uvedené!<br/><br/>"
                            ).replace(
            "<span>",
            '<span style="background-color:#ffff00;">'
            )
    elif importance_value == 3:
        importance = 'vysoka'
        email_body = email_body.replace("<div>",
                            "<div>Dobrý den,<br/>připomínám níže uvedené!!!!!<br/><br/>"
                            ).replace(
            "<span>",
            '<span style="background-color:#ffff00;">'
            )
    logger.debug(f"Email importance set: {importance_value} -> {importance}")
    return email_body

def previous_workday(exp_date: str):
    """calculate previous workday"""
    t = datetime.strptime(exp_date, "%d.%m.%Y")

    while True:
        t -= timedelta(days=1)
        # 0-4 = Po-Pá
        if t.weekday() < 5:
            logger.debug(f"expiration date set as: {t}")
            return t.strftime("%d.%m.%Y")