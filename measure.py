import os
import zipfile
import roifile

zipFilePath=r"C:\Users\jonme\Documents\School Work\Research - Bowman Lab\wagonWheelMeasurer\ignore\measurements.zip"
tempStoragePath=r"C:\Users\jonme\Documents\School Work\Research - Bowman Lab\wagonWheelMeasurer\ignore\temporaryRoiStorage"

with zipfile.ZipFile(zipFilePath, 'r') as zip_ref:
    zip_ref.extractall(tempStoragePath)

os.chdir(tempStoragePath)
fileNames = os.listdir()
coordList = []
for file in fileNames:
    coordList.append(roifile.ImagejRoi.fromfile(file).coordinates())
    #coordList.append(roifile.ImagejRoi.fromfile(file).coordinates().tolist())
    #^adding to      ^creating an object from         ^extracting the ^converting the numpy list
    #the list        the ROI file                     coordinates out  into a python list so it's
    #                                                 of that object   MATLAB readable

for file in fileNames:
    os.remove(file)

# with open("readme.txt","w") as readme:
#     readme.write("groups of roi files are stored in a .zip file.\nThis script needs a temporary place to store the unzipped ROIs while it runs.\nBecause this is a folder for temporary files, the contents are deleted every time you run measure.py\nDO NOT STORE ANYTHING IN THIS FOLDER. LET THE PROGRAM HANDLE IT.")
