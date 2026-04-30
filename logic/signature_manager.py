import constants as c

def save_signature(config, data, write_config):
    if c.SIGNATURE_SECTION not in config:
        raise ValueError("Chybí sekce SIGNATURE")

    for key, value in data.items():
        if value:
            config.set(c.SIGNATURE_SECTION, key, value)

    write_config(config, c.CONFIG_PATH)
def load_signature_data(config):
    name = config.get('SIGNATURE', 'name', fallback='')
    telephone = config.get('SIGNATURE', 'telephone', fallback='')
    department = config.get('SIGNATURE', 'department', fallback='')
    position = config.get('SIGNATURE', 'position', fallback='')
    login = config.get('SIGNATURE', 'login', fallback='')
    email = config.get('SIGNATURE', 'email', fallback='')
    return {'name':name,
            'department':department,
            'telephone':telephone,
            'position':position,
            'login':login,
            'email':email}