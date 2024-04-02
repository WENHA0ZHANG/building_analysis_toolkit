import csv
import datetime
from db_eplusout_reader import Variable, get_results
from db_eplusout_reader.constants import H

# Function to process the result_list
def process_data(lists):
    processed_lists = []
    for lst in lists:
        processed_list = [0 if 18 <= x <= 26 else 1 for x in lst]
        processed_lists.append(processed_list)
    return processed_lists

# Function to count the number 
def count_ones(processed_lists):
    return [sum(sublist) for sublist in processed_lists[1:]]

def after_energy_simulation():
    variables = [
        Variable(None, "Zone Mean Air Temperature", "C")
    ]

    results = get_results(api_environment.EnergyPlusFolder + r"eplusout.sql", variables=variables, frequency=H, alike=False)
    
    result_list = results.arrays
    variables = results.variables
    time_list = results.time_series
    name = ["Datetime"]
    processed_result_list = process_data(result_list)

    for i in range(len(variables)):
        name.append(variables[i].key)

    data_to_write = []

    for i in range(len(time_list)):
        row = [time_list[i].strftime("%Y-%m-%d %H:%M")] + [lst[i] for lst in processed_result_list]
        data_to_write.append(row)

    csv_file_path = api_environment.EnergyPlusFolder + r"Discomfort_Hour.csv"


    with open(csv_file_path, mode='wb') as file:
        writer = csv.writer(file)
        writer.writerow(name)  # Write the header
        writer.writerows(data_to_write)  # Write the data rows

# Write the counts to the txt file
    ones_counts = count_ones(processed_result_list)

    text_lines = [
        "{}: {}".format(header, count)  # Use format method instead of f-strings
        for header, count in zip(name[1:], ones_counts)  # Skip the 'Datetime' header
    ]

    txt_content = "\n".join(text_lines)

    txt_file_path = api_environment.EnergyPlusFolder + r"Custom_Comfort_Report.txt"

    with open(txt_file_path, 'wb') as file:
        file.write(txt_content)