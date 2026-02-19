import os
import tempfile

#atomicky zapis config.ini
def safe_write_config(config, path):
    dir_name = os.path.dirname(path) or "."

    with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            delete=False,
            dir=dir_name
    ) as tmp:
        config.write(tmp)#zapise se config do temp file
        temp_name = tmp.name #string s cestou k docasnemu souboru

    os.replace(temp_name, path)#smaze se puvodni config a nahradi temp file + prejmenuje

def safe_write_log(log,path):
    dir_name = os.path.dirname(path) or "."

    with tempfile.NamedTemporaryFile(
        mode='',
        encoding='',
        delete=False,
        dir=dir_name
    ) as tmp:
        log.write(tmp)
        temp_name = tmp.name

    os.replace(temp_name, path)
