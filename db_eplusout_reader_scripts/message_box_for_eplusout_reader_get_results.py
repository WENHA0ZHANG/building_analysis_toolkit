from db_eplusout_reader import Variable, get_results
from db_eplusout_reader.constants import RP
import ctypes
from os import path

def show_message(title, text):
    """Show message dialog."""
    ctypes.windll.user32.MessageBoxW(0, text, title, 0)


def after_energy_simulation():
    variables = [
        Variable("", "Electricity:Facility", "J")
    ]

    results = get_results(api_environment.EnergyPlusFolder + r"eplusout.sql", variables=variables, frequency=RP, alike=False)

    show_message("Information", "Successful access to data!")
