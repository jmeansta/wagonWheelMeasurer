import os
import zipfile
import roifile
import sys


#p1=r"C:\Users\jonme\Documents\School Work\Research - Bowman Lab\image analysis\roi python testing\\" + sys.argv[1]
#p1=r"C:\Users\jonme\Documents\School Work\Research - Bowman Lab\image analysis\images\Window C\\" + sys.argv[1]
p1=r"C:\Users\jonme\Documents\School Work\Research - Bowman Lab\image analysis\images\Window A\redone measurements\redone measurements.zip"
tempRoiStorage=r"C:\Users\jonme\Documents\School Work\Research - Bowman Lab\image analysis\roi python testing\temporaryRoiStorage"


with zipfile.ZipFile(p1, 'r') as zip_ref:
    zip_ref.extractall(tempRoiStorage)

os.chdir(tempRoiStorage)
fileNames = os.listdir()
coordList = []
for file in fileNames:
    #coordList.append(roifile.ImagejRoi.fromfile(file).coordinates())
    coordList.append(roifile.ImagejRoi.fromfile(file).coordinates().tolist())
    #^adding to      ^creating an object from         ^extracting the ^converting the numpy list
    #the list        the ROI file                     coordinates out  into a python list so it's
    #                                                 of that object   MATLAB readable

for file in fileNames:
    os.remove(file)
