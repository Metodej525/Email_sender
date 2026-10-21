import pytest
import configparser
import constants as c
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

class TestSheetManager:
    ...
