import pytest
import configparser
import constants as c
import pandas as pd

from Service.excel_service import ExcelLoader,SheetManager, initial_filter, excel_path_load,excel_search

@pytest.fixture
def setup_config():
    config = configparser.ConfigParser()
    config.add_section(c.EXCEL_SECTION)
    config.set(c.EXCEL_SECTION,c.EXCEL_PATH,"some path")
    return config

@pytest.fixture
def mock_app_state(mocker):
    mock = mocker.Mock()
    mock.set_df.side_effect = [RuntimeError("excel load failed"),True]
    return mock

@pytest.fixture
def mock_excel_raw_load(mocker):
    mock = mocker.Mock()
    return mock

@pytest.fixture
def excel_loader_instance(setup_config,
                          mock_app_state,
                          mock_excel_raw_load):
    return ExcelLoader(config=setup_config,
                       excel_raw_load=mock_excel_raw_load,
                       selected_sheet=1,
                       app_state=mock_app_state)

def test_excel_load(excel_loader_instance):

    with pytest.raises(RuntimeError,match="excel load failed"):
        excel_loader_instance.excel_load()
    excel_loader_instance.excel_load()
    excel_loader_instance.app_state.set_df.assert_called_with(
        excel_loader_instance.excel_raw_load.return_value
    )
@pytest.fixture
def create_test_excel(tmp_path,setup_config):
    file_path = tmp_path / "test_excel.xlsx"
    setup_config.set(c.EXCEL_SECTION, c.EXCEL_PATH, str(file_path))

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
    with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
        df1.to_excel(writer, index=False, sheet_name="Pololetí 1.")
        df2.to_excel(writer, index=False, sheet_name="Pololetí 2.")
    return df1,df2

@pytest.fixture
def sheet_manager(setup_config,create_test_excel):
    return SheetManager(setup_config)

class TestSheetManager:

    def test_sheet_checker(self,sheet_manager):
        assert sheet_manager.sheet_checker() == (["Pololetí 1.","Pololetí 2."],2)


def test_initial_filter(create_test_excel):
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
    pd.testing.assert_frame_equal(
        initial_filter(create_test_excel[0]),
        expected_df,
    )

def test_excel_search():
    ...