import pytest
import constants as c
import configparser

from Service.signature_service import save_signature,load_signature_data

# Fixture připraví konfigurační objekt se sekcí pro podpis.
@pytest.fixture
def setup_config():
    config = configparser.ConfigParser()
    config.add_section(c.SIGNATURE_SECTION)
    return config

# Mock nahrazuje funkci pro zápis konfigurace do souboru.
@pytest.fixture
def write_config_mock(mocker):
    return mocker.Mock()

# Ověření, že při chybějící sekci SIGNATURE funkce vyvolá ValueError.
def test_save_signature_value_error(write_config_mock,setup_config):
    setup_config.remove_section(c.SIGNATURE_SECTION)
    with pytest.raises(ValueError,match="Chybí sekce SIGNATURE"):
        save_signature(setup_config, {}, write_config_mock)

# Testuje ukládání různých hodnot podpisu, včetně prázdné hodnoty a None.
@pytest.mark.parametrize("data", [
    {"1": "x"},
    {"1": ""},
    {"1": "y"},
    {"1": None},
    {"1": "f"},
])
def test_save_signature(data,write_config_mock,setup_config):
    save_signature(setup_config,data,write_config_mock)
    # Ověří, že neprázdné hodnoty byly uloženy a prázdné hodnoty se neukládají.
    for key, value in data.items():
        if value:
            assert setup_config.get(c.SIGNATURE_SECTION, key) == value
        else:
            assert not setup_config.has_option(c.SIGNATURE_SECTION, key)

        # Kontrola, že zápis konfigurace proběhl právě jednou se správnými argumenty.
        write_config_mock.assert_called_once_with(setup_config, c.CONFIG_PATH)

# Ověření načtení jména podpisu z konfigurační sekce.
def test_load_signature_data(setup_config):
    setup_config.set(c.SIGNATURE_SECTION, c.SIGNATURE_NAME, "Jan")
    assert load_signature_data(setup_config)['name'] == 'Jan'