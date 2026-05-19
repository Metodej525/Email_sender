from datetime import timedelta, datetime
import constants as c
from utils import remove_diacritics
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
    raw_email_dict = get_emails(rows)
    checked_email_dict = email_none_state(raw_email_dict)


    for email,body in checked_email_dict.items():
        try:
            email_info = validate_email(str(email), check_deliverability=True)
            email = email_info.normalized
            checked_dict[email] = body
        except EmailNotValidError as e:
            print(e)
            continue

    return checked_dict

def email_sender(config,rows,toggle_value):
    """sends email/s"""
    checked_dict = check_email(rows)

    for email, body in checked_dict.items():
        body = importance_toggle(body,toggle_value)
        email_details(config, email, body)


def email_none_state(checked_dict):
    """checks and deletes None values from dict"""
    return {
        key: value
        for key, value in checked_dict.items()
        if key
    }
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


    return {'smtp_server': smtp_server,
            'smtp_port': smtp_port,
            'username': username,
            'sender_email': sender_email,
            'subject': subject,
            'body': f'{body1} datum {body2} datum {body3} {sign}'
            }
def specific_email_preview(config,exp_date,exp_time):
    """loads preview of email in specific row and returns it"""
    body1 = config.get(c.EMAIL_SECTION, c.EMAIL_BODY_1, fallback='')
    body2 = config.get(c.EMAIL_SECTION, c.EMAIL_BODY_2, fallback='')
    body3 = config.get(c.EMAIL_SECTION, c.EMAIL_BODY_3, fallback='')
    sign =  config.get(c.EMAIL_SECTION, c.EMAIL_SIGN, fallback='')
    minus_exp_date = previous_workday(exp_date)


    body = f'{body1} {exp_date} {exp_time} {body2} {minus_exp_date} {body3} {sign}'
    return body
def selected_value_manager(value):
    """loads on_select values and props them + makes email str"""
    raw_surname, raw_firstname, login, cert_type, exp = [x.strip() for x in value.split(',')]
    exp_date, exp_time = exp.split()
    surname = remove_diacritics(raw_surname.lower())
    firstname = remove_diacritics(raw_firstname.lower())

    email = f"{firstname}.{surname}@ikem.cz"
    print(email,exp_date, exp_time)
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

def importance_toggle(body,toggle_value):
    """Gives HTML text expect signature yellow background color"""
    if toggle_value == 2:
        return body.replace(
            "<span>",
            '<span style="background-color:#ffff00;">'
            )
    elif toggle_value == 3:
        return body.replace("<div>",
                            "<div>Dobrý den,<br/>připomínám níže uvedené!"
                            ).replace(
            "<span>",
            '<span style="background-color:#ffff00;">'
            )
    return body


def previous_workday(exp_date: str):
    """calculate previous workday"""
    t = datetime.strptime(exp_date, "%d.%m.%Y")

    while True:
        t -= timedelta(days=1)

        # 0-4 = Po-Pá
        if t.weekday() < 5:
            return t.strftime("%d.%m.%Y")


