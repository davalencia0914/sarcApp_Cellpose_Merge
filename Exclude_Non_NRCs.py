import os
import csv
import shutil

# Specify the folder paths
output_folder = '/Users/nakanolab/Desktop/20230519_+_+_NRC_WT_FHOD3L_Rescue_czi/ParticleTXT/'
destination_folder = '/Users/nakanolab/Desktop/20230519_+_+_NRC_FHOD3L_WT_Rescue_binary/Scaled_Binary/preSarcApp_CSVTestParticle/'
minimum_row_threshold = 11  # Minimum number of rows to consider

# Iterate over the CSV files in the output folder
for filename in os.listdir(output_folder):
    if filename.endswith('.csv'):
        csv_file_path = os.path.join(output_folder, filename)
        with open(csv_file_path, 'r') as file:
            csv_reader = csv.reader(file)
            row_count = sum(1 for row in csv_reader)

        # Check the row count against the threshold
        if row_count < minimum_row_threshold:
            # Move the file to the destination folder
            destination_path = os.path.join(destination_folder, filename)
            shutil.move(csv_file_path, destination_path)
            print(f"Moved file: {filename} to {destination_folder}")
