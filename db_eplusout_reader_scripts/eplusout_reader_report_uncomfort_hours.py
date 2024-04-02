from db_eplusout_reader import Variable, get_results
from db_eplusout_reader.constants import H
import ctypes
from os import path


def show_message(title, text):
    """Show message dialog."""
    ctypes.windll.user32.MessageBoxW(0, text, title, 0)


def count_temp(results_arrays,start_t, end_t):
    count = 0
    for i in range(start_t,end_t):
        if results_arrays[i]>=26 or results_arrays[i]<=26:
            count += 1
    return count

def after_energy_simulation():
    variables = [
        Variable("L0GROUNDFLOOR:OPENOFFICEN", "Zone Mean Air Temperature", "C")
    ]

    results = get_results(api_environment.EnergyPlusFolder + r"eplusout.sql", variables=variables, frequency=H, alike=False)
    results_arrays = results.arrays

    start_time = 5 # Enter the time when the building will begin operation, e.g. 5:00 = 5
    end_time = 18 # Enter the time at which the building will end its operation, e.g. 18:00 = 18
    sum_count = 0

    day_of_the_week  = 6 # Enter the start day of the week, e.g. Monday = 1, tuesday = 2, Sunday = 7 
    index = day_of_the_week -1
    for i in range(len(results_arrays[0])):
        if i!=0 and i%24 == 0:
            index += 1
            if index  > 7:
                show_message("Error", "Please input an integer between 1 and 7")
                break
            if index  == 6:
                continue
            elif index  == 7:
                index  = 0
                continue
            else:
                temp_list = results_arrays[0][i-24:i]
                count = count_temp(temp_list, start_time, end_time)
                sum_count += count

    show_message("Information", "Total uncomfort hours: " + str(sum_count))
