import pytest
import pandas as pd
from Repository.excel_repository import excel_raw_load

# Fixture vytvářející testovací Excelový soubor s ukázkovými daty
@pytest.fixture
def excel_file(tmp_path):
    file_path = tmp_path / "test_excel.xlsx"
    sheet_name = "1"

    # Vytvoření testovacího DataFrame se jmény a věkem
    df = pd.DataFrame({
        "name": ["Alice", "Bob"],
        "age": [25, 30],
    })

    # Uložení testovacích dat do Excelového souboru
    df.to_excel(file_path,sheet_name=sheet_name, index=False)

    return  df,file_path,sheet_name

# Test ověřující správné načtení dat z Excelového souboru
def test_excel_raw_load(excel_file):
    # Porovnání načteného DataFrame s původními testovacími daty
    pd.testing.assert_frame_equal(
        excel_raw_load(excel_file[1],excel_file[2]),
        excel_file[0],
    )
