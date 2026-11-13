import constants as c
import logging
import configparser

from datetime import timedelta, datetime
from collections.abc import Callable

from core.utilities import remove_diacritics
from core.protocols import EmailDataProtocol
#logger setup
logger = logging.getLogger(__name__)

class EmailConstructor:
    def __init__(self, config: configparser.ConfigParser,
                 data: list[EmailDataProtocol] | None,
                 importance_toggle: Callable[[str,int],str]
                 ) -> None:
        # Nastavení loggeru pro zaznamenávání událostí a chyb v tomto modulu.

        self.data = data
        self.config = config
        self.importance_toggle = importance_toggle

    def email_body_constructor(self,email_row:EmailDataProtocol) -> str:
        """Načte části textu e-mailu z konfigurace a sestaví výsledné tělo e-mailu."""
        # Načtení jednotlivých částí textu e-mailu; fallback zajistí prázdný řetězec,
        # pokud příslušná položka v konfiguraci chybí.
        body1 = self.config.get(c.EMAIL_SECTION, c.EMAIL_BODY_1, fallback='')
        body2 = self.config.get(c.EMAIL_SECTION, c.EMAIL_BODY_2, fallback='')
        body3 = self.config.get(c.EMAIL_SECTION, c.EMAIL_BODY_3, fallback='')
        sign = self.config.get(c.EMAIL_SECTION, c.EMAIL_SIGN, fallback='')

        # Výpočet předchozího pracovního dne podle data expirace.
        minus_exp_date = previous_workday(email_row.exp_date)

        # Sestavení těla e-mailu z textových částí a údajů konkrétního záznamu.
        email_body = f'{body1} {email_row.exp_date} {email_row.exp_time} {body2} {minus_exp_date} {body3} {sign}'
        return email_body

    def set_email_body(self) -> None:
        # Tělo e-mailu se vytváří pouze tehdy, pokud jsou vstupní data ve formě seznamu.
        if isinstance(self.data,list):
            for email_row in self.data:
                # Sestavení textu e-mailu pro konkrétní záznam.
                body = self.email_body_constructor(email_row)

                # Úprava textu podle nastavené důležitosti daného e-mailu.
                body = self.importance_toggle(body, email_row.importance)

                # Uložení výsledného textu přímo do příslušného záznamu.
                email_row.email_body = body
            logger.debug('email body constructed')
        else:
            logger.debug("no data to construct email body with")

class EmailSendManager:
    def __init__(self,config: configparser.ConfigParser,
                 email_data: list[EmailDataProtocol],
                 email_details: Callable[[configparser.ConfigParser,str,str],None],
                 ) -> None:
        self.config = config
        self.email_data =  email_data # Instance EmailData uložené v seznamu.
        self.email_details = email_details # Funkce zajišťující odeslání e-mailu.
        self.valid_data = []
        self.invalid_data = []

    def email_non_state_checker(self) -> None:
        """Rozdělí záznamy podle toho, zda obsahují e-mailovou adresu."""
        logger.debug('checked for none state in email dict')

        # Vymazání předchozích neplatných záznamů před novou kontrolou.
        self.invalid_data = []
        for email_row in self.email_data:
            # Záznam bez e-mailové adresy se zařadí mezi neplatná data.
            if email_row.email is None or email_row.email == '':
                self.invalid_data.append(email_row)
            else:
                # Záznam s vyplněnou e-mailovou adresou se zařadí mezi platná data.
                self.valid_data.append(email_row)
        logger.debug(f"valid data: {self.valid_data}")
        logger.debug('loaded email data non status checked')
        logger.debug("Invalid email data count: %s", len(self.invalid_data))

    def email_sender(self) -> None:
        # Nejprve rozdělí záznamy na platné a neplatné podle e-mailové adresy.
        self.email_non_state_checker()

        # Odeslání e-mailu pro každý záznam, který obsahuje e-mailovou adresu.
        for email_row in self.valid_data:
            self.email_details(self.config, email_row.email, email_row.email_body)
            logger.info(f"email sent to address: {email_row.email}")

def selected_value_manager(value: str) -> tuple[str, str, str]:
    """Zpracuje vybranou hodnotu a připraví údaje potřebné pro vytvoření e-mailové adresy."""
    # Rozdělení vstupního řetězce na jednotlivé údaje a odstranění okolních mezer.
    raw_surname, raw_firstname, login, cert_type, exp = [x.strip() for x in value.split(',')]

    # Rozdělení data a času expirace.
    exp_date, exp_time = exp.split()

    # Převedení jména a příjmení na malá písmena, nahrazení mezer tečkami
    # a odstranění české diakritiky.
    surname = remove_diacritics(raw_surname.lower().replace(' ','.'))
    firstname = remove_diacritics(raw_firstname.lower().replace(' ','.'))

    logger.debug("diacritics removed")

    # Sestavení e-mailové adresy podle jména a příjmení.
    email = f"{firstname}.{surname}@ikem.cz"
    logger.debug(f'email set as: {email}, exp_date as: {exp_date}, exp_time as: {exp_time}')
    return email, exp_date, exp_time

def previous_workday(exp_date: str) -> str:
    """Vypočítá předchozí pracovní den vzhledem k zadanému datu."""
    # Převod data z textového formátu na objekt datetime.
    t = datetime.strptime(exp_date, "%d.%m.%Y")

    while True:
        # Postupné posouvání data o jeden den zpět.
        t -= timedelta(days=1)

        # 0–4 představuje pondělí až pátek; víkend se přeskočí.
        if t.weekday() < 5:
            logger.debug(f"expiration date set as: {t}")
            return t.strftime("%d.%m.%Y")