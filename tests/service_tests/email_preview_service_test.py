import pytest
import configparser
import constants as c

from Service.email_preview_service import load_email_details

@pytest.fixture
def setup_config():
    config = configparser.ConfigParser()
    config.add_section(c.EMAIL_SECTION)
    return config

def test_load_email_details(setup_config):
    setup_config.set(c.EMAIL_SECTION, c.EMAIL_SMTP_SERVER, "0000")
    assert load_email_details(setup_config)['smtp_server'] == '0000'
    assert load_email_details(setup_config)['smtp_port'] == ''