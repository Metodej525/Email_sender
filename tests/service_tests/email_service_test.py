import pytest
import constants as c
import configparser
from gui.email_window import EmailData
from Service.email_service import EmailConstructor

@pytest.fixture
def setup_config():
    config = configparser.ConfigParser()
    config.add_section(c.EMAIL_SECTION)
    return config

@pytest.fixture
def mock_importance_toggle(mocker):
    mock = mocker.Mock()
    mock.return_value = "xx"
    return mock

@pytest.fixture
def email_data():
    return list((
                EmailData(exp_date='',
                    exp_time='',
                    email_body='y',
                    email='test1@test.com',
                    importance=1),
                EmailData(exp_date='',
                    exp_time='',
                    email_body='z',
                    email='test2@test.com',
                    importance=2),
                EmailData(exp_date='',
                    exp_time='',
                    email_body='a',
                    email='test3@test.com',
                    importance=3)
                 ))

@pytest.fixture
def email_constructor_class(setup_config,
                      email_data,
                      mock_importance_toggle):
    return EmailConstructor(setup_config,
                            email_data,
                            mock_importance_toggle)

def test_set_email_body(email_constructor_class,
                                monkeypatch):

    monkeypatch.setattr(
        email_constructor_class,
        "email_body_constructor",
        lambda email_row: "f"
    )
    email_constructor_class.set_email_body()
    assert email_constructor_class.data[0].email_body == 'xx'
