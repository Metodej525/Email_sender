import configparser

import pytest

from core.utilities import safe_write_config,remove_diacritics, importance_toggle


def test_safe_write_config_creates_config_file(tmp_path):
    """Write the configuration to a new file."""
    config = configparser.ConfigParser()
    config["settings"] = {"theme": "dark", "language": "en"}
    path = tmp_path / "config.ini"

    safe_write_config(config, str(path))

    saved_config = configparser.ConfigParser()
    saved_config.read(path, encoding="UTF-8")

    assert saved_config["settings"]["theme"] == "dark"
    assert saved_config["settings"]["language"] == "en"


remove_diacritics_values = [(4532,4532),("Metoděj","Metodej")]

@pytest.mark.parametrize("value,expected", remove_diacritics_values)
def test_remove_diacritics(value,expected):
    assert remove_diacritics(value) == expected


importance_toggle_values = [(2,"<div>Dobrý den,","<div>Dobrý den,<br/>připomínám níže uvedené!")
    ,(3,"<div>Dobrý den,","<div>Dobrý den,<br/>připomínám níže uvedené!!!!!")]

@pytest.mark.parametrize("toggle,value,expected",importance_toggle_values)
def test_importance_toggle(toggle,value,expected):
    assert importance_toggle(value,toggle) == expected