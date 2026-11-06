import pytest
import configparser
import constants as c

from infra.email_details import email_details

# Fixture připravující testovací konfiguraci pro odesílání e-mailů
@pytest.fixture
def setup_config():
    config = configparser.ConfigParser()

    # Vytvoření sekce s e-mailovým nastavením
    config.add_section(c.EMAIL_SECTION)

    # Nastavení testovacích SMTP údajů a parametrů e-mailu
    config.set(c.EMAIL_SECTION,c.EMAIL_SMTP_SERVER,"x")
    config.set(c.EMAIL_SECTION, c.EMAIL_SMTP_PORT, "999")
    config.set(c.EMAIL_SECTION, c.EMAIL_SENDER, "test_sender@test.cz")
    config.set(c.EMAIL_SECTION, c.EMAIL_SUBJECT, "test_subject")
    config.set(c.EMAIL_SECTION, c.EMAIL_CC, "test_sender@test.cz,"
                                            "test2_sender@test.cz,"
                                            "test3_sender@test.cz")

    return config

# Fixture vytvářející mock SMTP klienta a jeho serveru
@pytest.fixture
def test_mock_smtplib(mocker):
    mock_smtplib = mocker.MagicMock()
    mock_server = mocker.MagicMock()

    # Nastavení mock serveru jako návratové hodnoty SMTP kontextového manažeru
    mock_smtplib.SMTP.return_value.__enter__.return_value = mock_server

    return mock_smtplib

# Fixture nahrazující skutečnou SMTP knihovnu mock objektem
@pytest.fixture
def monkeypatch_smtplib(monkeypatch,test_mock_smtplib):
    monkeypatch.setattr("infra.email_details.smtplib",
                                test_mock_smtplib)

# Test ověřující správné zavolání metody pro odeslání e-mailu
def test_email_details(monkeypatch_smtplib,test_mock_smtplib,setup_config):
    # Zavolání funkce s testovací konfigurací a obsahem e-mailu
    email_details(setup_config,"reciever@test.cz","email body")

    # Získání instance mock SMTP serveru
    server = test_mock_smtplib.SMTP.return_value.__enter__.return_value

    # Ověření, že metoda sendmail byla zavolána právě jednou
    server.sendmail.assert_called_once()