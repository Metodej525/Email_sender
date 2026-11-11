import logging
import pytest
from core.initial_setup import setup_config, setup_logger
import configparser
from types import SimpleNamespace

# Poskytuje mock logger pro testování logovacích operací
# bez vytváření skutečných logovacích záznamů.
@pytest.fixture
def mock_logger(mocker):
    mock = mocker.Mock()

    return mock

# Nahrazuje modul logging mock objektem, jehož metoda getLogger()
# vrací připravený mock logger.
@pytest.fixture
def mock_logging(mocker,mock_logger):
    mock = mocker.Mock()
    mock.getLogger.return_value = mock_logger
    return mock

# Vytváří platný INI konfigurační soubor v dočasném adresáři
# pro ověření správného načtení konfigurace.
@pytest.fixture
def setup_valid_config_ini(tmp_path):
    config = configparser.ConfigParser()

    # Vytvoření sekce a jejích konfiguračních hodnot.
    config.add_section('section')
    config['section']['setting_1'] = "hello"
    config['section']['setting_2'] = "goodbye"

    # Uložení konfigurace do dočasného souboru.
    with open(tmp_path / "config.ini", mode='w') as f:
        config.write(f)

# Vytváří neplatný INI soubor pro testování chování
# při chybě parsování konfigurace.
@pytest.fixture
def setup_invalid_config_ini(tmp_path):


    with open(tmp_path / "config.ini", mode='w') as file:
        file.write("Hello")

# Připravuje izolované prostředí pro testování setup_config().
# Nahrazuje závislosti na systémových cestách a loggeru
# pomocí monkeypatch, aby testy nebyly závislé na prostředí aplikace.
@pytest.fixture
def setup_config_monkeypatch(tmp_path,monkeypatch,mock_logger):
    config_path = "config.ini"

    # Nastavení cesty ke konfiguračnímu souboru.
    monkeypatch.setattr("core.initial_setup.c.CONFIG_PATH",
                        config_path)
    # Simulace spuštění programu jako Python script.
    monkeypatch.setattr("core.initial_setup.sys.executable",
                        tmp_path)
    # Nastavení základní složky aplikace pro případ spuštění jako .exe.
    monkeypatch.setattr("core.initial_setup.c.BASE_DIR",
                        tmp_path)
    # Nahrazení skutečného loggeru mock objektem.
    monkeypatch.setattr("core.initial_setup.logger",
                        mock_logger)

# Ověřuje správné ošetření situace, kdy konfigurační soubor
# není nalezen, a kontroluje zaznamenání odpovídající chybové zprávy.
def test_setup_config_invalid_path(setup_config_monkeypatch,
                      monkeypatch,
                      mock_logger):
    mock_path = "test"

    # Simulace neplatné cesty ke konfiguračnímu souboru.
    monkeypatch.setattr("core.initial_setup.sys.executable",
                        mock_path)

    # Nahrazení loggeru mock objektem.
    monkeypatch.setattr("core.initial_setup.logger",
                        mock_logger)

    # Nastavení neexistující cesty ke konfiguračnímu souboru.
    monkeypatch.setattr("core.initial_setup.c.CONFIG_PATH",
                        mock_path)

    # Zavolání testované funkce.
    setup_config()

    # Ověření, že logger zaznamenal přesně jednu chybovou zprávu.
    mock_logger.error.assert_called_once_with("Config file not found")

# Ověřuje úspěšné načtení platného konfiguračního souboru
# a zaznamenání informační zprávy o jeho načtení.
def test_setup_config_valid_path(setup_config_monkeypatch,
                                 mock_logger,
                                 setup_valid_config_ini,
                                 tmp_path):
    # Zavolání testované funkce.
    setup_config()

    # Ověření, že při načítání konfigurace nedošlo k chybě.
    mock_logger.error.assert_not_called()

    # Ověření, že logger zaznamenal informaci o úspěšném načtení.
    mock_logger.info.assert_called_once_with(
        f"Config loaded with {tmp_path / 'config.ini'}"
    )

# Ověřuje správné ošetření neplatného formátu konfigurace
# a zaznamenání odpovídající chybové zprávy.
def test_setup_config_invalid_format(setup_config_monkeypatch,
                                     mock_logger,
                                     setup_invalid_config_ini):
    # Zavolání testované funkce.
    setup_config()

    mock_logger.error.assert_called_once()
    error_message = mock_logger.error.call_args[0][0]


    assert error_message.startswith("Config failed parsing with exception:")

# Připravuje izolované prostředí pro testování setup_logger().
# Nahrazuje standardní logging jednoduchým objektem,
# aby bylo možné kontrolovat chování loggeru bez zásahu
# do skutečného logovacího systému aplikace.
@pytest.fixture
def setup_logger_monkeypatch(monkeypatch, mock_logger, tmp_path):

    fake_logging = SimpleNamespace(
        getLogger=lambda *args: mock_logger,
        INFO=logging.INFO
    )

    monkeypatch.setattr(
        "core.initial_setup.logging",
        fake_logging
    )

    # Přesměrovává výstup logování do dočasného adresáře.
    monkeypatch.setattr(
        "core.initial_setup.c.LOG_PATH",
        tmp_path / "logs/logs.jsonl"
    )

# Ověřuje, že již nakonfigurovaný logger zůstane beze změny
# a nedojde k opakovanému přidání handleru ani změně úrovně logování.
def test_valid_setup_logger(setup_logger_monkeypatch, mock_logger):


    mock_logger.handlers = [object()]
    result = setup_logger()


    assert result is mock_logger

    mock_logger.addHandler.assert_not_called()
    mock_logger.setLevel.assert_not_called()
    
# Ověřuje správnou inicializaci loggeru, který dosud neobsahuje
# žádné handlery, včetně nastavení úrovně logování INFO.
def test_invalid_setup_logger(setup_logger_monkeypatch, mock_logger):

    mock_logger.handlers = []
    result = setup_logger()

    assert result is mock_logger

    mock_logger.addHandler.assert_called_once()
    mock_logger.setLevel.assert_called_once_with(
        logging.INFO
    )
    mock_logger.debug.assert_called_once_with("logger set")