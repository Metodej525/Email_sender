from core.initial_setup import setup_logger, setup_config
from core.gui_setup import setup_gui
from core.app_state import  AppState

def main():
    state = AppState() #inicializace app state pro zapis dataframu
    setup_logger() #inicializace logu
    config = setup_config() #config.ini nacteni
    setup_gui(config, state) #inicializace gui

if __name__ == "__main__":
    main()