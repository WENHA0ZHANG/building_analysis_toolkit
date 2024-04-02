import ctypes
from eppy.results import readhtml
from os import path


def show_message(title, text):
    """Show message dialog."""
    ctypes.windll.user32.MessageBoxW(0, text, title, 0)


def after_energy_simulation():
    tablePath = api_environment.EnergyPlusFolder + r"eplustbl.htm"
    if path.exists(tablePath):
        filehandle = open(tablePath, 'r').read()
        if filehandle is not None:
            htables = readhtml.titletable(filehandle)
            firstitem = htables[0]
            firstitem_table = firstitem[1]
            thirdrow = firstitem_table[2]
            thirdrow_secondcolumn = thirdrow[1]
            net_site_energy = str(thirdrow_secondcolumn)
            show_message("Information", "Net Site Energy: " + net_site_energy + " MJ/m2")

        else:
            show_message("Information", "Error creating TableReader")
    else:
        show_message("Information", "File does not exist " + tablePath)