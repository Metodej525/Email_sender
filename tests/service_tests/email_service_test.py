import pytest
import constants as c
import configparser
from gui.email_window import EmailData
from Service.email_service import EmailConstructor, EmailSendManager, selected_value_manager, previous_workday


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
def multiple_email_data():
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
                    email='',
                    importance=3)
                 ))

@pytest.fixture
def email_constructor__instance(setup_config,
                      multiple_email_data,
                      mock_importance_toggle):
    return EmailConstructor(setup_config,
                            multiple_email_data,
                            mock_importance_toggle)
class TestEmailConstructor:

    def test_set_email_body(self,email_constructor_instance, mocker):
        mock = mocker.patch.object(
            email_constructor_instance,
            "email_body_constructor",
            return_value="f"
        )

        email_constructor_instance.set_email_body()

        assert mock.call_count == 3
        assert all(
            row.email_body == "xx"
            for row in email_constructor_instance.data
        )

    def test_email_body_constructor(self,email_constructor_instance,
                                    setup_config,
                                    monkeypatch):
        setup_config.set(c.EMAIL_SECTION,c.EMAIL_BODY_1,'a')
        setup_config.set(c.EMAIL_SECTION, c.EMAIL_BODY_2, 'b')
        setup_config.set(c.EMAIL_SECTION, c.EMAIL_BODY_3, 'c')
        setup_config.set(c.EMAIL_SECTION, c.EMAIL_SIGN, 'x')

        monkeypatch.setattr("Service.email_service.previous_workday",
                            lambda previous_workday: '3')
        assert email_constructor_instance.email_body_constructor(
            EmailData(exp_date='1',
                        exp_time='2',
                        email_body='',
                        email='test1@test.com',
                        importance=1)) == "a 1 2 b 3 c x"
@pytest.fixture
def mock_email_details(mocker):
    mock = mocker.Mock()
    return mock

@pytest.fixture
def email_send_manager_instance(setup_config,
                       multiple_email_data,
                       mock_email_details):
    return EmailSendManager(setup_config,multiple_email_data,mock_email_details)

class TestEmailSenderManager:

    def test_email_non_state_checker(self,email_send_manager_instance):
        email_send_manager_instance.email_non_state_checker()
        assert email_send_manager_instance.invalid_data == [EmailData(exp_date='',
                    exp_time='',
                    email_body='a',
                    email='',
                    importance=3)]
        assert email_send_manager_instance.valid_data == [EmailData(exp_date='',
                    exp_time='',
                    email_body='y',
                    email='test1@test.com',
                    importance=1),
                EmailData(exp_date='',
                    exp_time='',
                    email_body='z',
                    email='test2@test.com',
                    importance=2)]

    def test_email_sender(self,email_send_manager_instance
                          ,mock_email_details,
                          setup_config):
        email_send_manager_instance.email_sender()
        assert mock_email_details.call_count == 2

values = [("Novák, Tomáš, novt, Q-TW-CZ, 18.06.2026 15:22:00",
           "tomas.novak@ikem.cz","18.06.2026","15:22:00"),
          ("Paleta, Luboš, pall, Q-TW-CZ, 20.08.2030 18:05:00",
           "lubos.paleta@ikem.cz", "20.08.2030", "18:05:00")
          ]
@pytest.mark.parametrize("value,email,exp_date,exp_time",values)
def test_selected_value_manager(value,
                                email,
                                exp_date,
                                exp_time):
    expected = (email,
                exp_date,
                exp_time)

    assert selected_value_manager(value) == expected

def test_previous_workday():
    ...