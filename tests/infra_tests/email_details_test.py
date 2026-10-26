import pytest
import configparser
import constants as c

from infra.email_details import email_details

@pytest.fixture
def setup_config():
    config = configparser.ConfigParser()

    config.add_section(c.EMAIL_SECTION)

    config.set(c.EMAIL_SECTION,c.EMAIL_SMTP_SERVER,"x")
    config.set(c.EMAIL_SECTION, c.EMAIL_SMTP_PORT, "999")
    config.set(c.EMAIL_SECTION, c.EMAIL_SENDER, "test_sender@test.cz")
    config.set(c.EMAIL_SECTION, c.EMAIL_SUBJECT, "test_subject")
    config.set(c.EMAIL_SECTION, c.EMAIL_CC, "test_sender@test.cz,"
                                            "test2_sender@test.cz,"
                                            "test3_sender@test.cz")

    return config
@pytest.fixture
def test_mock_smtplib(mocker):
    mock_smtplib = mocker.MagicMock()
    mock_server = mocker.MagicMock()

    mock_smtplib.SMTP.return_value.__enter__.return_value = mock_server

    return mock_smtplib

@pytest.fixture
def monkeypatch_smtplib(monkeypatch,test_mock_smtplib):
    monkeypatch.setattr("infra.email_details.smtplib",
                                test_mock_smtplib)

def test_email_details(monkeypatch_smtplib,test_mock_smtplib,setup_config):
    email_details(setup_config,"reciever@test.cz","email body")
    server = test_mock_smtplib.SMTP.return_value.__enter__.return_value
    server.sendmail.assert_called_once()