def save_signature(config, data, write_config):
    if "SIGNATURE" not in config:
        raise ValueError("Chybí sekce SIGNATURE")

    for key, value in data.items():
        if value:
            config.set("SIGNATURE", key, value)

    write_config(config, "config.ini")
