from eppy.results import readhtml
from os import path
import shutil
import os

folder_path = api_environment.EnergyPlusFolder
folder_name = "Results"
new_folder_path = os.path.join(folder_path, folder_name)
os.makedirs(new_folder_path)

list_id = []
list_value = []

def after_energy_simulation():
    tablePath = api_environment.EnergyPlusFolder + r"eplustbl.htm"
    filehandle = open(tablePath, 'r').read()
    htables = readhtml.lines_table(filehandle)
    first_table = htables[0]
    simulation_time = first_table[0][3][26:34].replace(":", "_")
    destination_path = os.path.join(new_folder_path, simulation_time + "_eplustbl.htm")
    shutil.copy(tablePath, destination_path)

    ltables = readhtml.titletable(filehandle)
    firstitem = ltables[0]
    firstitem_table = firstitem[1]
    thirdrow = firstitem_table[2]
    thirdrow_secondcolumn = thirdrow[1]
    net_site_energy = str(thirdrow_secondcolumn)
    list_id.append(simulation_time)
    list_value.append(net_site_energy)

    file_name = os.path.join(new_folder_path, "results.txt")
    with open(file_name, "w") as file:
        for id, value in zip(list_id, list_value):
            file.write('Iteration ID: ' + str(id) + '; ' + 'Net site energy: ' + str(value) + '\n')

