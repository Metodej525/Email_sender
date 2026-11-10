import pytest
from core.initial_setup import setup_config, setup_logger
import configparser

@pytest.fixture
def mock_logger(mocker,monkeypatch):
    mock = mocker.Mock()
    return mock

@pytest.fixture
def setup_valid_config_ini(tmp_path):
    config = configparser.ConfigParser()

    config.add_section('section')
    config['section']['setting_1'] = "hello"
    config['section']['setting_2'] = "goodbye"

    with open(tmp_path / "config.ini", mode='w') as f:
        config.write(f)

@pytest.fixture
def setup_invalid_config_ini(tmp_path):


    with open(tmp_path / "config.ini", mode='w') as file:
        file.write("Hello")

@pytest.fixture
def setup_config_monkeypatch(tmp_path,monkeypatch,mock_logger):
    config_path = "config.ini"
    monkeypatch.setattr("core.initial_setup.c.CONFIG_PATH",
                        config_path)
    # nastavení monkeypatch pro spuštění jako script
    monkeypatch.setattr("core.initial_setup.sys.executable", tmp_path)
    # nastavení monkeypatch pro spuštění jako .exe
    monkeypatch.setattr("core.initial_setup.c.BASE_DIR", tmp_path)
    # mock loggeru
    monkeypatch.setattr("core.initial_setup.logger", mock_logger)

def test_setup_config_invalid_path(setup_config_monkeypatch,
                      monkeypatch,
                      mock_logger):
    mock_path = "test"

    # nastavení monkeypatch pro spuštění jako script
    monkeypatch.setattr("core.initial_setup.sys.executable", mock_path)
    # mock loggeru
    monkeypatch.setattr("core.initial_setup.logger", mock_logger)
    # mock neexistující cesty k .ini
    monkeypatch.setattr("core.initial_setup.c.CONFIG_PATH",
                        mock_path)

    setup_config()
    mock_logger.error.assert_called_once_with("Config file not found")

def test_setup_config_valid_path(setup_config_monkeypatch,
                                 mock_logger,
                                 setup_valid_config_ini,
                                 tmp_path):
    setup_config()
    mock_logger.error.assert_not_called()
    mock_logger.info.assert_called_once_with(
        f"Config loaded with {tmp_path / 'config.ini'}"
    )

def test_setup_config_invalid_format(setup_config_monkeypatch,
                                     mock_logger,
                                     setup_invalid_config_ini):
    setup_config()
    mock_logger.error.assert_called_once()
    error_message = mock_logger.error.call_args[0][0]

    assert error_message.startswith("Config failed parsing with exception:")


# @pytest.fixture
# def setup_logger_monkeypatch(monkeypatch,
#                              mock_logger,
#                              tmp_path):
#     monkeypatch.setattr("core.initial_setup.logging",mock_logger)
#     monkeypatch.setattr("core.initial_setup.c.LOG_PATH",tmp_path / "logs/logs.jsonl")
#
# def test_valid_setup_logger(setup_logger_monkeypatch,
#                             mock_logger):
#
#     mock_logger.handlers.return_value = False
#     setup_logger()
#     mock_logger.setLevel.assert_called()
# def test_invalid_setup_logger(setup_logger_monkeypatch,
#                             mock_logger):
#
#     setup_logger()
#     mock_logger.addHandler.assert_called()