import sys
import numpy as np
import os
from alpha_shapes.alpha_shapes import Alpha_Shaper
import pickle
from scipy import ndimage
import glob
from matplotlib import pyplot as plt
    
outputFolder = "filepath_to_output_folder"
count = 1
array_filepath = glob.glob(os.path.join("filepath_to_folder_of_NPY_files", '*.npy'))
array_dict = {f1: np.load(f1, allow_pickle=True, fix_imports=True) for f1 in array_filepath}

# Move Alpha_Shaper object definition outside the function
shaper = None
    
def cellposeEdge(npy_file, outputFolder, count, xres, scale):
    mask = np.load(npy_file, allow_pickle=True, fix_imports=True, encoding='bytes').item()
    binary_mask = mask['outlines']
    filled = ndimage.binary_fill_holes(mask['outlines'])
    labels, num_features = ndimage.label(filled)
    objects = np.zeros((labels.shape[0], labels.shape[1], num_features))
    
    for i in range(np.max(labels)):
        print(i)
        mask = (labels == i+1)
        objects[:,:,i] = mask*1
    
    for obj in range(objects.shape[2]):
        print(obj)
        coords = np.where(objects[:,:,obj] > 0)
        coords = np.flip(coords, axis=0)
        x = coords[0] / xres
        y = coords[1] / xres
        
        if len(x) < 4 or len(y) < 4:
            continue
        else:
            points = np.stack((x, y), axis=1)
            
            # Check if points are empty
            if points.size == 0:
                continue

            alpha = 6.0
            while alpha > 0:
                shaper = Alpha_Shaper(points)
                alpha_shape = shaper.get_shape(alpha=alpha)
                try:
                    edgeX, edgeY = alpha_shape.exterior.coords.xy
                except AttributeError:
                    alpha -= 1
                else:
                    break
            
            edgeX = np.array(edgeX)
            edgeY = np.array(edgeY)
            cx = sum(edgeX) / len(edgeX)
            cy = sum(edgeY) / len(edgeY)
            edgeX = (scale * (edgeX - cx)) + cx
            edgeY = (scale * (edgeY - cy)) + cy
            # Construct output file path
            output_filename = f"edgeShape_{os.path.splitext(filename)[0]}_{count}.pickle".format(obj)
            outputFilePath = os.path.join(outputFolder, output_filename)
            print("Output File Path:", outputFilePath)
            count += 1
            os.makedirs(outputFolder, exist_ok=True)
            
            try:
                with open(outputFilePath, "wb") as f:
                    pickle.dump(alpha_shape, f)
            except Exception as e:
                print("Error occurred while saving pickle file:", str(e))
    return edgeX, edgeY, alpha_shape
for npy_file in array_dict:
    try:
        # Extract the filename from the file path
        filename = os.path.basename(npy_file)
        cellposeEdge(npy_file, outputFolder, count, xres=6.2016, scale=1.1)
    except RuntimeError as e:
        print("Error occurred while processing", npy_file)
        try:
            print(traceback.format_exc())  # Print the traceback for detailed error information
        except NameError:
            print("An error occurred while printing the traceback. Please enable verbose mode to see the original qhull error.")
        continue
print("Pickle files saved in the designated output folder:", outputFolder)
