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
# def safe_write_log(logs,path):
#     dir_name = os.path.dirname(path) or "."
#
#     with tempfile.NamedTemporaryFile(
#         mode='',
#         encoding='UTF-8',
#         delete=False,
#         dir=dir_name
#     ) as tmp:
#         logs.write(tmp)
#         temp_name = tmp.name
#
#     os.replace(temp_name, path)

def remove_diacritics(text):
    if not isinstance(text, str):
        return text
    # Normalizace na NFD (rozdělí znaky + diakritiku)
    normalized = unicodedata.normalize('NFD', text)
    # Vrátí jen znaky, které nejsou "Mn" (Mark, Nonspacing = diakritika)
    return ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')