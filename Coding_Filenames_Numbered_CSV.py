import os
import csv

# Specify the folder path
folder_path = "/Users/dylanvalencia/Desktop/20230820_+_+_WT_BioRep1_SarcApp/20230820_+_+_WT_BioRep1_preSarcAppCSV_SufficientHA_Coded/"

# Get the list of files within the folder
file_list = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

# Sort the file list alphanumerically
file_list.sort()

# Create a dictionary to store the key (original filename) and value (renamed filename)
key = {}

# Initialize the counter
count = 0

# Rename the files and store the key-value pairs
for filename in file_list:
    # Skip the .DS_Store file and empty directories
    if filename == '.DS_Store' or os.path.getsize(os.path.join(folder_path, filename)) == 0:
        continue
    # Exclude empty directories
    if os.path.getsize(os.path.join(folder_path, filename)) == 0:
        continue

    # Generate the renamed filename
    renamed_filename = f'{count}.csv'  # Adjust the file extension if needed

    # Rename the file
    original_file_path = os.path.join(folder_path, filename)
    renamed_file_path = os.path.join(folder_path, renamed_filename)
    os.rename(original_file_path, renamed_file_path)

    # Store the key-value pair in the dictionary
    key[renamed_filename] = filename
    
    # Increment the counter
    count += 1
# Save the key-value pairs to a CSV file
key_csv_file = os.path.join(folder_path, 'key.csv')
with open(key_csv_file, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerows(key.items())

print("Files renamed successfully.")
print("Original filenames and their corresponding new names are saved in 'key.csv'.")
