from datetime import timedelta, datetime
import constants as c
from core.utilities import remove_diacritics


import logging

logger = logging.getLogger(__name__)


class EmailSendManager:
    def __init__(self,config,email_data,email_details):
        self.config = config
        self.email_data =  email_data #EmailData instances wrapped in list
        self.email_details = email_details #INFRA email function
        self.valid_data = []

    def email_body_constructor(self,email_row):
        """loads preview of email in specific row and returns it"""
        body1 = self.config.get(c.EMAIL_SECTION, c.EMAIL_BODY_1, fallback='')
        body2 = self.config.get(c.EMAIL_SECTION, c.EMAIL_BODY_2, fallback='')
        body3 = self.config.get(c.EMAIL_SECTION, c.EMAIL_BODY_3, fallback='')
        sign = self.config.get(c.EMAIL_SECTION, c.EMAIL_SIGN, fallback='')
        minus_exp_date = previous_workday(email_row.exp_date)
        email_body = f'{body1} {email_row.exp_date} {email_row.exp_time} {body2} {minus_exp_date} {body3} {sign}'
        return email_body

    def importance_toggle(self,email_body,importance_value):
        """Gives HTML text expect signature yellow background color"""
        importance = 'nizka'
        if importance_value == 2:
            importance = 'stredni'
            email_body = email_body.replace("<div>Dobrý den,",
                                            "<div>Dobrý den,<br/>připomínám níže uvedené!"
                                            ).replace(
                "<span>",
                '<span style="background-color:#ffff00;">'
            )
        elif importance_value == 3:
            importance = 'vysoka'
            email_body = email_body.replace("<div>Dobrý den,",
                                            "<div>Dobrý den,<br/>připomínám níže uvedené!!!!!"
                                            ).replace(
                "<span>",
                '<span style="background-color:#ffff00;">'
            )
        logger.debug(f"Email importance set: {importance_value} -> {importance}")
        return email_body
    def set_email_body(self):
        for email_row in self.email_data:
            body = self.email_body_constructor(email_row)
            body = self.importance_toggle(body, email_row.importance)

            email_row.email_body = body

    def email_non_state_checker(self):
        """checks and deletes None values from dict"""
        logger.debug('checked for none state in email dict')
        invalid_data = []
        for email_row in self.email_data:
            if email_row.email is None or email_row.email == '':
                invalid_data.append(email_row)
            else:
                self.valid_data.append(email_row)

    def prepare_data(self):
        self.email_non_state_checker()
        self.set_email_body()
    def email_sender(self):
        for email_row in self.valid_data:
            self.email_details(self.config, email_row.valid_email, email_row.email_body)
            logger.info(f"send email to: {email_row.valid_email}")

def selected_value_manager(value):
    """loads on_select values and props them + makes email str"""
    raw_surname, raw_firstname, login, cert_type, exp = [x.strip() for x in value.split(',')]
    exp_date, exp_time = exp.split()
    surname = remove_diacritics(raw_surname.lower().replace(' ','.'))
    firstname = remove_diacritics(raw_firstname.lower().replace(' ','.'))
    logger.debug("diacritics removed")
    email = f"{firstname}.{surname}@ikem.cz"
    logger.debug(f'email set as: {email}, exp_date as: {exp_date}, exp_time as: {exp_time}')
    return email, exp_date, exp_time

def previous_workday(exp_date: str):
    """calculate previous workday"""
    t = datetime.strptime(exp_date, "%d.%m.%Y")

    while True:
        t -= timedelta(days=1)
        # 0-4 = Po-Pá
        if t.weekday() < 5:
            logger.debug(f"expiration date set as: {t}")
            return t.strftime("%d.%m.%Y")