
def save_signature(config, data, write_config):
    if "SIGNATURE" not in config:
        raise ValueError("Chybí sekce SIGNATURE")

    for key, value in data.items():
        if value:
            config.set("SIGNATURE", key, value)

    write_config(config, "config.ini")
def load_signature_data(config):
    name = config.get('SIGNATURE', 'name', fallback='')
    telephone = config.get('SIGNATURE', 'telephone', fallback='')
    department = config.get('SIGNATURE', 'department', fallback='')
    position = config.get('SIGNATURE', 'position', fallback='')
    login = config.get('SIGNATURE', 'login', fallback='')
    return {'name':name,
            'department':department,
            'telephone':telephone,
            'position':position,
            'login':login}