from eppy.results import readhtml
from os import path
import shutil
import os

folder_path = api_environment.EnergyPlusFolder
folder_name = "Results"
new_folder_path = os.path.join(folder_path, folder_name)
os.makedirs(new_folder_path)

def after_energy_simulation():
    tablePath = api_environment.EnergyPlusFolder + r"eplustbl.htm"
    filehandle = open(tablePath, 'r').read()
    htables = readhtml.lines_table(filehandle)
    first_table = htables[0]
    simulation_time = first_table[0][3][26:34].replace(":", "_")
    destination_path = os.path.join(new_folder_path, simulation_time + "_eplustbl.htm")
    shutil.copy(tablePath, destination_path)