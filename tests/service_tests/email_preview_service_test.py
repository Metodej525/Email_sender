import pytest
import configparser
import constants as c

# Import funkce pro načtení e-mailových nastavení z konfigurace
from Service.email_preview_service import load_email_details

# Fixture připravující základní testovací konfiguraci
@pytest.fixture
def setup_config():
    config = configparser.ConfigParser()

    # Vytvoření sekce obsahující e-mailová nastavení
    config.add_section(c.EMAIL_SECTION)
    return config

# Test ověřující správné načtení e-mailových údajů z konfigurace
def test_load_email_details(setup_config):

    # Nastavení testovací hodnoty SMTP serveru
    setup_config.set(c.EMAIL_SECTION, c.EMAIL_SMTP_SERVER, "0000")

    # Ověření správného načtení nastavené hodnoty SMTP serveru
    assert load_email_details(setup_config)['smtp_server'] == '0000'

    # Ověření výchozí prázdné hodnoty nenastaveného SMTP portu
    assert load_email_details(setup_config)['smtp_port'] == ''