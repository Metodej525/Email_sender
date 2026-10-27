import os
import tempfile
import unicodedata
import logging

logger = logging.getLogger(__name__)

def safe_write_config(config, path):
    """Write a configuration file atomically.

    The configuration is first written to a temporary file in the
    destination directory. Once writing succeeds, the temporary file
    replaces the destination file atomically.

    Args:
        config: A configuration object supporting the ``write()`` method.
        path: Path to the destination configuration file.
    """
    dir_name = os.path.dirname(path) or "."
    temp_name = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="UTF-8",
            delete=False,
            dir=dir_name,
        ) as tmp:
            config.write(tmp)
            temp_name = tmp.name

        # Replace the destination only after the temporary file is closed.
        os.replace(temp_name, path)
        logger.debug("Safely wrote configuration to: %s", path)

    finally:
        # Remove the temporary file if writing or replacement failed.
        if temp_name is not None and os.path.exists(temp_name):
            os.unlink(temp_name)

def remove_diacritics(text):
    """Remove diacritical marks from a string.

    Return the input unchanged if it is not a string.
    """
    if not isinstance(text, str):
        return text

    # Decompose characters into their base characters and combining marks.
    normalized = unicodedata.normalize("NFD", text)

    # Remove all nonspacing marks (category "Mn"), including diacritical marks.
    return "".join(
        c for c in normalized
        if unicodedata.category(c) != "Mn"
    )

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