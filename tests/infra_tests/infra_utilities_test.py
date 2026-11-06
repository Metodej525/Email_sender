import pytest

# Import funkce pro převod textu do HTML formátu
from infra.infra_utilities import html_converter

# Testovací hodnoty ověřující převod různých typů zalomení řádků
values = [
    ("\r\n\r\n aaa \r\n\r\n", "<p></p><p> aaa </p><p></p>"),
    ("\n\n aaa \n\n", "<p></p><p> aaa </p><p></p>"),
    ("\r\n aaa \r\n", "<p><br> aaa <br></p>"),
    ("\n aaa \n", "<p><br> aaa <br></p>"),
]

# Parametrizovaný test ověřující správný převod textu do HTML
@pytest.mark.parametrize("text,expected",values)
def test_html_converter(text,expected):
    # Porovnání výsledného HTML s očekávaným výstupem
    assert html_converter(text) == expected
