from gui.gui import Gui
from main import calculate_and_print_specification
from logging import basicConfig, INFO


basicConfig(level=INFO,
            filename=f"log/log_for_gui.log",
            filemode="w")
gui = Gui(calculate_and_print_specification)
