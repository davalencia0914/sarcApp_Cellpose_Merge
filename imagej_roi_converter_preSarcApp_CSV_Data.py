from ij import IJ
from ij.plugin.frame import RoiManager
from ij.gui import PolygonRoi
from ij.gui import Roi
from java.awt import FileDialog
import os
from ij import IJ, ImagePlus, WindowManager

def process_file(input_dir, input_txt_dir, output_dir, file_name, txt_file_path):
    # Open the TIFF file in ImageJ
    imp = IJ.openImage(os.path.join(input_dir, file_name))
    if imp is not None:
        imp.show()
        try:
            # Set AutoThreshold
            IJ.setAutoThreshold(imp, "Default dark no-reset")

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
                            continue # Skip the invalid line and continue with the next line
                            #There may be a way to skip the No images open window on imageJ when this occurs, but currently it has to be manually closed for the program to continue
                textfile.close()
                rm.runCommand("Associate", "true")
                rm.runCommand("Show All with labels")
            except IOError:
                print("Failed to open TXT file:", txt_file_path)
            except Exception as e:
                print("An error occurred:", str(e))
                # Handle the exception (e.g., log the error, continue with the next image)

            finally:
                # Set the measurements
                IJ.run("Set Measurements...", "area centroid bounding fit shape feret's integrated redirect=None decimal=3")

                # Get the number of ROIs
                roi_count = rm.getCount()

                # Set the minimum area threshold (change this value as needed)
                minimum_area_threshold = 1  #To remove undersegmented ROIs from Cellpose, but I currently do this manually by eye
                    
                # Iterate over each ROI
                r = 0
                for r in range(roi_count):
                    rm.setSelectedIndexes([r])  # Select the ROI at index r
                    current_roi = rm.getRoi(r)

                    if isinstance(current_roi, PolygonRoi):
                        # Get the area of the current ROI
                        area = current_roi.getStatistics().area

                        if area >= minimum_area_threshold:
                            # Perform operations on ROIs that meet the area threshold
                            IJ.run("Analyze Particles...", "display include")
                            prefixR = os.path.splitext(file_name)[0]
                            csv_file_name = prefixR + "_seg_" + str(r+1) + ".csv"
                            csv_file_path = os.path.join(output_dir, csv_file_name)
                            IJ.saveAs("Results", csv_file_path)
                            IJ.run("Close")
                        r += 1  # Move to the next ROI
                    else:
                        # Delete ROIs of unsupported type
                        rm.runCommand("Delete")
                        roi_count -= 1  # Decrement the total ROI count
                rm.runCommand("Reset")
                IJ.run("Close")
                rm.runCommand("Close")
                IJ.run("Close All", "")
                rm.runCommand("Reset")
                rm.runCommand("Close")
            imp.changes = False  # Mark the image as unchanged to prevent "No images open" dialog
            imp.close()  # Ensure that the image is closed even if an exception occurs

        except Exception as e:
            print("An error occurred:", str(e))
            # Handle the exception (e.g., log the error, continue with the next image)
    else:
        print("Failed to open TIFF image:", file_name)

# Main code
#input dir for binary images
input_dir = "/Users/dylanvalencia/Desktop/20230820_+_-_KD_SarcApp_BioRep1/20230820_+_-_KD_Scaled_Binaries_ManualContrast/"
#input txt dir for the txt files corresponding to those binary images
input_txt_dir = "/Users/dylanvalencia/Desktop/20230820_+_-_KD_SarcApp_BioRep1/20230820_+_-_KD_TXT_Files_Filtered/"
#output dir for csv files to use in SarcApp
output_dir = "/Users/dylanvalencia/Desktop/20230820_+_-_KD_SarcApp_BioRep1/+_-_KD_ManualContrastBinary_preSarcApp_CSV/"
#change filepaths accordingly each time

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

list_files = os.listdir(input_dir)
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
    # Get the corresponding txt file path
    txt_file_name = prefix + "_cp_outlines.txt"
    txt_file_path = os.path.join(input_txt_dir, txt_file_name)
    if txt_file_name in txt_files:
        # Process the file
        process_file(input_dir, input_txt_dir, output_dir, file_name, txt_file_path)
    else:
        print("TXT file not found for" + txt_file_name)
    print(file_name)
