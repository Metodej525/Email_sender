import pytest
import constants as c
import configparser

from Service.signature_service import save_signature,load_signature_data

@pytest.fixture
def setup_config():
    config = configparser.ConfigParser()
    config.add_section(c.SIGNATURE_SECTION)
    return config

@pytest.fixture
def write_config_mock(mocker):
    return mocker.Mock()

def test_save_signature_value_error(write_config_mock,setup_config):
    setup_config.remove_section(c.SIGNATURE_SECTION)
    with pytest.raises(ValueError,match="Chybí sekce SIGNATURE"):
        save_signature(setup_config, {}, write_config_mock)

@pytest.mark.parametrize("data", [
    {"1": "x"},
    {"1": ""},
    {"1": "y"},
    {"1": None},
    {"1": "f"},
])
def test_save_signature(data,write_config_mock,setup_config):
    save_signature(setup_config,data,write_config_mock)
    for key, value in data.items():
        if value:
            assert setup_config.get(c.SIGNATURE_SECTION, key) == value
        else:
            assert not setup_config.has_option(c.SIGNATURE_SECTION, key)
        write_config_mock.assert_called_once_with(setup_config, c.CONFIG_PATH)

def test_load_signature_data(setup_config):
    setup_config.set(c.SIGNATURE_SECTION, c.SIGNATURE_NAME, "Jan")
    assert load_signature_data(setup_config)['name'] == 'Jan'