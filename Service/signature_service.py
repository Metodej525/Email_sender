import constants as c

def save_signature(config, data, write_config):
    if c.SIGNATURE_SECTION not in config:
        raise ValueError("Chybí sekce SIGNATURE")

    for key, value in data.items():
        if value:
            config.set(c.SIGNATURE_SECTION, key, value)

    write_config(config, c.CONFIG_PATH)
def load_signature_data(config):
    name = config.get(c.SIGNATURE_SECTION, c.SIGNATURE_NAME, fallback='')
    telephone = config.get(c.SIGNATURE_SECTION, c.SIGNATURE_TELEPHONE, fallback='')
    department = config.get(c.SIGNATURE_SECTION, c.SIGNATURE_DEPARTMENT, fallback='')
    position = config.get(c.SIGNATURE_SECTION, c.SIGNATURE_POSITION, fallback='')
    login = config.get(c.SIGNATURE_SECTION, c.SIGNATURE_LOGIN, fallback='')
    email = config.get(c.SIGNATURE_SECTION, c.SIGNATURE_EMAIL, fallback='')
    return {'name':name,
            'department':department,
            'telephone':telephone,
            'position':position,
            'login':login,
            'email':email}