import os
import tempfile
import unicodedata
import logging

logger = logging.getLogger(__name__)

#atomicky zapis config.ini
def safe_write_config(config, path):
    dir_name = os.path.dirname(path) or "."

    with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="UTF-8",
            delete=False,
            dir=dir_name
    ) as tmp:
        config.write(tmp)#zapise se config do temp file
        temp_name = tmp.name #string s cestou k docasnemu souboru

    os.replace(temp_name, path)#smaze se puvodni config a nahradi temp file + prejmenuje
    logger.debug(f"safely wrote into config: {path}")

def remove_diacritics(text):
    if not isinstance(text, str):
        return text
    # Normalizace na NFD (rozdělí znaky + diakritiku)
    normalized = unicodedata.normalize('NFD', text)
    # Vrátí jen znaky, které nejsou "Mn" (Mark, Nonspacing = diakritika)
    return ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')

def importance_toggle(email_body,importance_value):
    """Gives HTML text expect signature yellow background color"""
    importance = 'nizka'
    if importance_value == 2:
        importance = 'stredni'
        email_body = email_body.replace("<div>Dobrý den,",
                                        "<div>Dobrý den,<br/>připomínám níže uvedené!"
                                        ).replace(
            "<span>",
            '<span style="background-color:#ffff00;">'
        )
    elif importance_value == 3:
        importance = 'vysoka'
        email_body = email_body.replace("<div>Dobrý den,",
                                        "<div>Dobrý den,<br/>připomínám níže uvedené!!!!!"
                                        ).replace(
            "<span>",
            '<span style="background-color:#ffff00;">'
        )
    logger.debug(f"Email importance set: {importance_value} -> {importance}")
    return email_body