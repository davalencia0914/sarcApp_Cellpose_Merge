from ij import IJ
from ij.plugin.frame import RoiManager
from ij.plugin import ChannelSplitter
from ij.measure import Measurements
from ij.measure import ResultsTable
from ij.plugin.filter import Analyzer
from ij.gui import PolygonRoi
from ij.gui import Roi
from java.awt import FileDialog
import os



def process_file(input_dir, input_txt_dir, output_dir, file_name, txt_file_path):
    # Open the TIFF file in ImageJ
    imp = IJ.openImage(os.path.join(input_dir, file_name))
    if imp is not None:
        imp.show()
        rt = None  # Define the 'rt' variable outside the try block
        try:
            channels = ChannelSplitter.split(imp);
            
            # Select the channel you want to perform measurements on
            channel_index = 0  # Replace 0 with the desired channel index (e.g., 0 for the first channel, in this case HA-FHOD3L intensities)
            selected_channel = channels[channel_index]
            # Access the txt file name from the list
            txt_file_name = os.path.basename(txt_file_path)

            # Run the imageJ_roi_converter.py macro
            RM = RoiManager()
            rm = RM.getRoiManager()
            
            try:
                textfile = open(txt_file_path, "r")
                for line in textfile:
                    values = line.rstrip().split(",")
                    if len(values) >= 2:  # Check if the line contains at least two values
                        try:
                            xy = list(map(int, values))
                            X = xy[::2]
                            Y = xy[1::2]
                            imp.setRoi(PolygonRoi(X, Y, Roi.POLYGON))
                            roi = imp.getRoi()
                            print(roi)
                            rm.addRoi(roi)
                        except ValueError:
                            print("Skipping line with invalid format:", line)
                            continue  # Skip the invalid line and continue with the next line
                            # There may be a way to skip the No images open window on imageJ when this occurs, but currently it has to be manually closed for the program to continue
                textfile.close()
                rm.runCommand("Associate", "true")
                rm.runCommand("Show All with labels")
            except IOError:
                print("Failed to open TXT file:", txt_file_path)
            except Exception as e:
                print("An error occurred:", str(e))
                # Handle the exception (e.g., log the error, continue with the next image)

            finally:
                # Set measurement options
                IJ.run("Set Measurements...", "area mean min integrated redirect=None decimal=3")
                
                # Get the number of ROIs
                roi_count = rm.getCount()
                # Iterate over each ROI
                r = 0
                for r in range(roi_count):
                    rm.setSelectedIndexes([r])  # Select the ROI at index r
                    current_roi = rm.getRoi(r)
                    rm.runCommand(selected_channel,"Measure")
                    prefixR = os.path.splitext(file_name)[0]
                    csv_file_name = prefixR + "_seg_" + str(r+1) + "_HA_Intensity.csv"
                    csv_file_path = os.path.join(output_dir, csv_file_name)
                    IJ.saveAs("Results", csv_file_path)
                    IJ.run("Close")
                r += 1  # Move to the next ROI
                rm.runCommand("Reset")
                IJ.run("Close")
                rm.runCommand("Close")
                IJ.run("Close All", "")
                #Run other Python script to filter through single cell csv data files for sufficiently sized cells that are expressing exogenous FHOD3L well (HAFHOD3L_CSV_Filtering.txt in iPython)
            imp.changes = False  # Mark the image as unchanged to prevent "No images open" dialog
            imp.close()  # Ensure that the image is closed even if an exception occurs
            selected_channel.changes = False  # Mark the image as unchanged to prevent "No images open" dialog
            selected_channel.close()  # Ensure that the image is closed even if
        except Exception as e:
            print("An error occurred:", str(e))
            # Handle the exception (e.g., log the error, continue with the next image)
    else:
        print("Failed to open TIFF image:", file_name)
            
# Main code
input_dir = "/Users/nakanolab/Desktop/Actinin+_+/"
#Input dir for CZI files
input_txt_dir = "/Users/nakanolab/Desktop/+_+WT_NewTXTWhole_FilteredNoArtifacts/"
#input txt dir for txt files of outlines
output_dir = "/Users/nakanolab/Desktop/Actinin+_+/HAFHOD3L+_+_WT_CSV_SingleCell/"
#change filepaths accordingly each time

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

list_files = os.listdir(input_dir) #Lists out the czi files in the folder
txt_files = []  # List to store txt file names

# Iterate through txt files in the input_txt_dir
for file_name in os.listdir(input_txt_dir):
    if file_name.endswith(".txt"):
        # Add the txt file name to the list
        txt_files.append(file_name)
        
for file_name in list_files:
    base_name = file_name.split(".")
    prefix = base_name[0]
    found_file = False  # Flag to track if a valid file is found
    txt_file_name = prefix + "_cp_outlines.txt"
    txt_file_path = os.path.join(input_txt_dir, txt_file_name)
    if txt_file_name in txt_files:
        # Process the file
        process_file(input_dir, input_txt_dir, output_dir, file_name, txt_file_path)
    else:
        print("No TXT file found for " + prefix)
    print(file_name)
