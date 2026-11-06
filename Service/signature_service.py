import constants as c

def save_signature(config, data, write_config):
    # Kontrola, zda v konfiguraci existuje sekce pro podpis.
    # Pokud chybí, vyvolá se výjimka ValueError.
    if c.SIGNATURE_SECTION not in config:
        raise ValueError("Chybí sekce SIGNATURE")

    # Procházení jednotlivých údajů podpisu.
    for key, value in data.items():
        # Do konfigurace se ukládají pouze vyplněné hodnoty.
        if value:
            config.set(c.SIGNATURE_SECTION, key, value)

    # Uložení aktualizované konfigurace do konfiguračního souboru.
    write_config(config, c.CONFIG_PATH)


def load_signature_data(config):
    # Načtení jednotlivých údajů podpisu z konfigurace.
    # Pokud některá položka neexistuje, použije se prázdný řetězec.
    name = config.get(c.SIGNATURE_SECTION, c.SIGNATURE_NAME, fallback='')
    telephone = config.get(c.SIGNATURE_SECTION, c.SIGNATURE_TELEPHONE, fallback='')
    department = config.get(c.SIGNATURE_SECTION, c.SIGNATURE_DEPARTMENT, fallback='')
    position = config.get(c.SIGNATURE_SECTION, c.SIGNATURE_POSITION, fallback='')
    login = config.get(c.SIGNATURE_SECTION, c.SIGNATURE_LOGIN, fallback='')
    email = config.get(c.SIGNATURE_SECTION, c.SIGNATURE_EMAIL, fallback='')

    # Vrácení všech načtených údajů ve formě slovníku.
    return {'name':name,
            'department':department,
            'telephone':telephone,
            'position':position,
            'login':login,
            'email':email}