from core.initial_setup import setup_logger, setup_config
from core.gui_setup import setup_gui


def main():
    setup_logger() #inicializace logu
    config = setup_config() #config.ini nacteni
    setup_gui(config) #inicializace gui

if __name__ == "__main__":
    main()