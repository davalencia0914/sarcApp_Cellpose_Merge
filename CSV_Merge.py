import os
import re
import csv

# Specify the folder path containing the CSV files
folder_path = '/Users/dylanvalencia/Desktop/20230820_+_+_WT_BioRep1_SarcApp/20230820_+_+_WT_Pickles_SufficientHA_Coded_SarcAppDataOutput/'

# Specify the output merged CSV file path
merged_csv_path = '/Users/dylanvalencia/Desktop/20230820_+_+_WT_BioRep1_SarcApp/20230820_+_+_WT_Pickles_SufficientHA_Coded_SarcAppDataOutput/20230820_+_+_WT_mergedcellResults.csv'

# Specify the common prefix of the files, whether its cell, mf, or msf
file_prefix = 'actinin_cellResults'

# Get the list of CSV files in the folder
csv_files = [filename for filename in os.listdir(folder_path) if filename.startswith(file_prefix) and filename.endswith('.csv')]

# Define the regular expression pattern to extract the numeric part
pattern = re.compile(r'^{}(\d+).csv$'.format(file_prefix))

# Extract the numeric part from each filename and convert it to an integer
file_numbers = [int(re.match(pattern, filename).group(1)) for filename in csv_files]

# Sort the CSV files based on the numeric part of the filename
sorted_csv_files = [filename for _, filename in sorted(zip(file_numbers, csv_files))]

# Initialize a list to store the data from each file
merged_data = []

# Iterate over the sorted CSV files
for filename in sorted_csv_files:
    csv_file_path = os.path.join(folder_path, filename)
    with open(csv_file_path, 'r') as file:
        csv_reader = csv.reader(file)
        data = list(csv_reader)

    # Insert the filename as the first row in the data
    data.insert(0, [filename])

    # Add the data to the merged_data list
    merged_data.extend(data)

# Write the merged data to the output CSV file
with open(merged_csv_path, 'w', newline='') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerows(merged_data)

print("Merging of CSV files completed!")
