import pytest
import pandas as pd
from Repository.excel_repository import excel_raw_load

@pytest.fixture
def excel_file(tmp_path):
    file_path = tmp_path / "test_excel.xlsx"
    sheet_name = "1"

    df = pd.DataFrame({
        "name": ["Alice", "Bob"],
        "age": [25, 30],
    })
    df.to_excel(file_path,sheet_name=sheet_name, index=False)

    return  df,file_path,sheet_name


def test_excel_raw_load(excel_file):
    pd.testing.assert_frame_equal(
        excel_raw_load(excel_file[1],excel_file[2]),
        excel_file[0],
    )
