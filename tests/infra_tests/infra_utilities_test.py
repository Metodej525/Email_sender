import pytest

from infra.infra_utilities import html_converter
values = [
    ("\r\n\r\n aaa \r\n\r\n", "<p></p><p> aaa </p><p></p>"),
    ("\n\n aaa \n\n", "<p></p><p> aaa </p><p></p>"),
    ("\r\n aaa \r\n", "<p><br> aaa <br></p>"),
    ("\n aaa \n", "<p><br> aaa <br></p>"),
]

@pytest.mark.parametrize("text,expected",values)
def test_html_converter(text,expected):
    assert html_converter(text) == expected
