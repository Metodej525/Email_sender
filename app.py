from core.initial_setup import setup_logger, setup_config
from core.gui_setup import setup_gui

#inicializace logu
setup_logger()

#config.ini nacteni
config = setup_config()

#inicializace gui
setup_gui(config)








