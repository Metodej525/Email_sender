import pytest
import configparser
import constants as c
import pandas as pd

from Service.excel_service import ExcelLoader,SheetManager, initial_filter, excel_path_load,excel_search

# Fixture připravující testovací konfiguraci pro práci s Excelem
@pytest.fixture
def setup_config():
    config = configparser.ConfigParser()
    config.add_section(c.EXCEL_SECTION)
    config.set(c.EXCEL_SECTION,c.EXCEL_PATH,"some path")
    return config

# Fixture vytvářející mock aplikačního stavu
# První volání set_df vyvolá chybu, druhé proběhne úspěšně
@pytest.fixture
def mock_app_state(mocker):
    mock = mocker.Mock()
    mock.set_df.side_effect = [RuntimeError("excel load failed"),True]
    return mock

# Fixture vytvářející mock funkce pro načtení surových Excelových dat
@pytest.fixture
def mock_excel_raw_load(mocker):
    mock = mocker.Mock()
    return mock

# Fixture vytvářející instanci ExcelLoader s testovacími závislostmi
@pytest.fixture
def excel_loader_instance(setup_config,
                          mock_app_state,
                          mock_excel_raw_load):
    return ExcelLoader(config=setup_config,
                       excel_raw_load=mock_excel_raw_load,
                       selected_sheet=1,
                       app_state=mock_app_state)

# Test ověřující správné zpracování chyby a následné úspěšné načtení Excelu
def test_excel_load(excel_loader_instance):
    # Ověření, že první načtení vyvolá očekávanou výjimku
    with pytest.raises(RuntimeError,match="excel load failed"):
        excel_loader_instance.excel_load()

    # Opakované načtení po prvním neúspěšném pokusu
    excel_loader_instance.excel_load()

    # Ověření předání načtených dat do aplikačního stavu
    excel_loader_instance.app_state.set_df.assert_called_with(
        excel_loader_instance.excel_raw_load.return_value
    )

# Fixture vytvářející testovací Excelový soubor se dvěma listy
@pytest.fixture
def create_test_excel(tmp_path,setup_config):
    file_path = tmp_path / "test_excel.xlsx"
    setup_config.set(c.EXCEL_SECTION, c.EXCEL_PATH, str(file_path))

    # Testovací data prvního pololetí
    df1 = pd.DataFrame({
    "Řešitel": ["technik1", "technik2"],
    "Příjmení": ["Paleta", "Novák"],
    "Jméno":["Franta","Jarda"],
    "Login":["pafr","naja"],
    "Sériové číslo":["1256532","4561531"],
    "Typ cert.":["Q-TW-CZ","Q-PE:RS-CZ"],
    "Platnost do":["02.01.2026 08:14:00","02.01.2026 09:46:00"],
    "Termín":["","prodlužuje si sám"],
    "Poznámka":["",""],
    })

    # Testovací data druhého pololetí
    df2 = pd.DataFrame({
        "Řešitel": ["technik2", "technik1"],
        "Příjmení": ["Vokoun", "Skrblík"],
        "Jméno": ["Martin", "František"],
        "Login": ["pafr", "naja"],
        "Sériové číslo": ["4587453", "6587452"],
        "Typ cert.": ["Q-TW-CZ", "Q-TW-CZ"],
        "Platnost do": ["07.01.2026 09:35:00", "10.01.2026 08:16:00"],
        "Termín": ["", ""],
        "Poznámka": ["", ""],
    })

    # Uložení obou DataFrame do samostatných listů Excelového souboru
    with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
        df1.to_excel(writer, index=False, sheet_name="Pololetí 1.")
        df2.to_excel(writer, index=False, sheet_name="Pololetí 2.")
    return df1,df2

# Fixture vytvářející instanci správce Excelových listů
@pytest.fixture
def sheet_manager(setup_config,create_test_excel):
    return SheetManager(setup_config)

class TestSheetManager:

    # Test ověřující správné získání názvů listů a jejich celkového počtu
    def test_sheet_checker(self,sheet_manager):
        assert sheet_manager.sheet_checker() == (["Pololetí 1.","Pololetí 2."],2)

# Test ověřující filtrování Excelových dat podle definovaných podmínek
def test_initial_filter(create_test_excel):
    # Očekávaný výsledek po aplikaci filtru
    expected_df = pd.DataFrame({
    "Řešitel": ["technik1"],
    "Příjmení": ["Paleta"],
    "Jméno":["Franta"],
    "Login":["pafr"],
    "Sériové číslo":["1256532"],
    "Typ cert.":["Q-TW-CZ"],
    "Platnost do":["02.01.2026 08:14:00"],
    "Termín":[""],
    "Poznámka":[""],
    })

    # Porovnání výsledného DataFrame s očekávanými daty
    pd.testing.assert_frame_equal(
        initial_filter(create_test_excel[0]),
        expected_df,
    )

# Test ověřující vyhledávání záznamu podle uživatelského loginu
def test_excel_search(create_test_excel):
    assert excel_search('pafr',create_test_excel[0]) == [('Paleta',
                                                          'Franta',
                                                          'pafr',
                                                          'Q-TW-CZ',
                                                          '02.01.2026 08:14:00')]

# Test ověřující aktualizaci cesty k Excelovému souboru v konfiguraci
def test_excel_path_load(setup_config,mocker):
    setup_config.clear()
    path = "some path"
    safe_write_config_mock = mocker.Mock()

    # Ověření vyvolání chyby při chybějící konfigurační sekci
    with pytest.raises(ValueError,match="Chybí sekce EXCEL"):
        excel_path_load(setup_config,path,safe_write_config_mock)

    # Doplnění potřebné sekce a původní cesty k souboru
    setup_config.add_section(c.EXCEL_SECTION)
    setup_config.set(c.EXCEL_SECTION, c.EXCEL_PATH, path)

    # Ověření, že při nezměněné cestě nedochází k zápisu konfigurace
    excel_path_load(setup_config,path,safe_write_config_mock)
    safe_write_config_mock.assert_not_called()

    # Změna cesty a ověření aktualizace konfigurace
    excel_path_load(setup_config, "not some path", safe_write_config_mock)
    assert setup_config.get(c.EXCEL_SECTION, c.EXCEL_PATH) == "not some path"

    # Ověření, že změna cesty vyvolala právě jeden zápis konfigurace
    safe_write_config_mock.assert_called_once_with(
        setup_config, c.CONFIG_PATH
    )
