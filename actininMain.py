from Dataset import Dataset
from actininFixed2D import actininFixed2D
from binaryMeasure import binaryMeasure
from makeBinary import makeBinary
from prepareData import prepareData
from getMetadata import getMetadata
import csv
import numpy as np
import os
import glob

    
def actininMain(folders, dtype, uploadBools):
    if (dtype == 'Fixed 2D'):
        loader = Dataset(folders)
        totalCellStats = []
        outputFolder = folders['-OUT-']
        if uploadBools[2]:
            for i in range(len(loader)):
                image, binary, data_path = loader[i]
                if image is not None:
                    xres = getMetadata(image)
                elif binary is not None:
                    xres = getMetadata(binary)
                numData, headerKeys = prepareData(data_path)
                if uploadBools[0]:
                    cellStats = actininFixed2D(i, numData, headerKeys, uploadBools, outputFolder, image, xres)
                elif uploadBools[1]:
                    cellStats = actininFixed2D(i, numData, headerKeys, uploadBools, outputFolder, binary, xres)
                elif uploadBools[2]:
                    #pickle_list = glob.glob(os.path.join(outputFolder, '*.pickle'))
                    #pickle_dict = {f1: np.load(f1, allow_pickle=True, fix_imports=True) for f1 in pickle_list}
                    #for filename_pickle in pickle_list:
                        # Extract the filename from the pickle file path
                    #filename_pickle = os.path.basename(filename_pickle)
                        # Extract the prefix from the pickle filename
                    #csv_prefix = filename_pickle.split("edgeShape_")[1].split(".pickle")[0]
                        # Construct the CSV filename using the prefix
                    #filename_csv = csv_prefix + ".csv"
                        #csv_filepaths = [os.path.join(data_path, filename_csv)]
                        ###for csv_filepath in csv_filepaths:
                        #base_filename = os.path.splitext(os.path.basename(csv_filepath))[0]
                        #pickle_filename = "edgeShape_{}.pickle".format(csv_prefix)
                    #print(filename_pickle + " in for loop Main")
                    #pickle_filepath = os.path.join(outputFolder, filename_pickle)
                        #if os.path.exists(pickle_filepath):
                            # Extract the prefix from the pickle filename
                   # pickle_prefix = pickle_filename.split("edgeShape_")[1].split(".pickle")[0]
                            # Extract the prefix from the CSV filename
                            #csv_prefix = pickle_filename
                    #print(csv_prefix + " is the csv prefix under if os.path statement")
                            # Check if the prefixes match
                            #if pickle_prefix == csv_prefix:
                                # Call actininFixed2D only if the prefixes match
                    cellStats = actininFixed2D(i, numData, headerKeys, uploadBools, outputFolder, display=None, xres=1)
                            #else:
                             #   print("Prefix mismatch for pickle file and CSV file:", pickle_prefix, csv_prefix)
                        #else:
                           # print("Pickle file not found:", pickle_filepath)
                    totalCellStats.append(cellStats)
        else:
            if uploadBools[1]:
                for i in range(len(loader)):
                    img, bin, data = loader[i]
                    xres = getMetadata(bin)
                    numData, headerKeys = binaryMeasure(bin, xres)
                    cellStats = actininFixed2D(i, numData, headerKeys, uploadBools, outputFolder, bin, xres)
                    totalCellStats.append(cellStats)
            elif uploadBools[0]:
                for i in range(len(loader)):
                    image, bin, data = loader[i]
                    xres = getMetadata(image)
                    numData, headerKeys, bin = makeBinary(image, xres)
                    cellStats = actininFixed2D(i, numData, headerKeys, uploadBools, outputFolder, image, xres)
                    totalCellStats.append(cellStats)
                    
        cellHeaders = ['Cell','Myofibrils','Total Z-lines',
            'Average Myofibril Persistence Length','Average Z-Line Length', 
            'Average Z-Line Spacing','Average Size of All Puncta', 'Total Puncta',
            'MSFs', 'Total Z-Bodies', 'Average MSF Persistence Length', 
            'Average Z-Body Length', 'Average Z-Body Spacing']
        folderHeaders = ['Average Myofibrils/Cell','Average Z-Lines/Cell',
            'Average Myofibril Persistence Length','Average Z-Line Length', 
            'Average Z-Line Spacing','Average Size of All Puncta', 'Average Puncta/Cell',
            'Average MSFs/Cell', 'Average Z-Bodies/Cell', 'Average MSF Persistence Length', 
            'Average Z-Body Length', 'Average Z-Body Spacing']

        path1 = os.path.join(outputFolder, "actinin_totalResults.csv")
        with open(path1,'w', newline='') as f:
            write = csv.writer(f)
            write.writerow(cellHeaders)
            write.writerows(totalCellStats)
        totalCellStats = np.asarray(totalCellStats)
        totalCellStats = totalCellStats[:,1:]
        folderMeans = np.nanmean(totalCellStats,axis=0)

        path2 = os.path.join(outputFolder, "actinin_folderMeans.csv")
        with open(path2,'w', newline='') as f:
            write = csv.writer(f)
            write.writerow(folderHeaders)
            write.writerow(folderMeans)
