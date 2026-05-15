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

def email_sender(config,rows,toggle):
    """sends email/s"""
    checked_dict = check_email(rows)

    for email, body in checked_dict.items():
        if toggle:
            body = importance_toggle(body)
        email_details(config, email, body)


def email_none_state(checked_dict):
    return {
        key: value
        for key, value in checked_dict.items()
        if key
    }
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
def importance_toggle(body):
#     body = """<div>
# <p>Dobrý den,<br/><br/><font style=background-color:yellow;><b>blíží se konec platnosti vašeho certifikátu</b> na e-podpis (28.5.). <b>Dostavte se, prosím, co nejdříve</b> (nejpozději dne <b>27.5.</b>) s čipovou kartou na Odbor informatiky - dveře <b>A4015</b> (vedle stříbrné poštovní schránky), provedeme prodloužení platnosti. Musíte znát PIN karty.<br/>Přijďte v pracovní dny ideálně mezi 8:30 – 11:30 a 12:30 - 15:45.</font><br/><br/>Certifikáty prodlužují: Komínková Ilona, Zoth Jindřich nebo Kopec Michal.<br/><b>V případě naší nepřítomnosti zajděte na sekretariát OI dveře A4002 – k asistence Kláře Tiché (linka 4200).</b></p>
# </div>"""
    return body

#     return body.replace(
#         "<span>",
#         """
# <font style="background-color:#fff59d;">"""
#     ).replace(
#         '</span>',
#         """
#         </font>
#         """
#
#     )
    # return body.replace(
    #     "<span>",
    #     """<table cellspacing="0" cellpadding="0" style="display:inline;">
    #     <tr>
    #     <td bgcolor="yellow">"""
    # ).replace(
    #     '</span>',
    #     """
    #     </td>
    #         </tr>
    #         </table>
    #     """
    #
    # )
def previous_workday(exp_date: str):
    t = datetime.strptime(exp_date, "%d.%m.%Y")

    while True:
        t -= timedelta(days=1)

        # 0-4 = Po-Pá
        if t.weekday() < 5:
            return t.strftime("%d.%m")


