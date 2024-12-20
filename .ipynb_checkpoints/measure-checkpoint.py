import os
import zipfile
import roifile
import numpy as np
import shapely

#TODO:
# Implement Readme: 
    # with open("readme.txt","w") as readme:
    # readme.write("groups of roi files are stored in a .zip file.\n
    # This script needs a temporary place to store the unzipped ROIs while it runs.\n
    # Because this is a folder for temporary files, the contents are deleted every time you run measure.py\n
    # DO NOT STORE ANYTHING IN THIS FOLDER. LET THE PROGRAM HANDLE IT.")
# import numpy in a more standard way
# upgrade to a more current version of python
# add validation for file reading and deletion
# add GUI and increase general user-friendliness
# add pixels to real measurements conversion


zipFilePath=r"C:\Users\jonme\Documents\School Work\Research - Bowman Lab\wagonWheelMeasurer\ignore\measurements.zip"
tempStoragePath=r"C:\Users\jonme\Documents\School Work\Research - Bowman Lab\wagonWheelMeasurer\ignore\temporaryRoiStorage"
saveFilePath=r"C:\Users\jonme\Documents\School Work\Research - Bowman Lab\wagonWheelMeasurer\ignore\measurements.txt"

def rotMatrix(theta):
    # returns a numpy rotation matrix at the given angle (radians)
    theta = np.degrees(theta)
    return np.matrix([[np.cos(theta),-np.sin(theta)],[np.sin(theta),np.cos(theta)]])

def yIntercept(x1,y1,x2,y2):
    # returns the y-intercept of a line given two points on it
    return -x1*((y2-y1)/(x2-x1))+y1

with zipfile.ZipFile(zipFilePath, 'r') as zip_ref:
    zip_ref.extractall(tempStoragePath)

os.chdir(tempStoragePath)
fileNames = os.listdir()
roiList = []
for file in fileNames:
    roiList.append(roifile.ImagejRoi.fromfile(file).coordinates())
for file in fileNames:
    os.remove(file)

with open(saveFilePath,"a") as saveFile:
    saveFile.write("ROI Name,Angle,Diameter(px)\n")
    for roiCoords,roiName in zip(roiList,fileNames):
        roiCoords = np.append(roiCoords,[roiCoords[0]], axis=0)
        roiPoly = shapely.Polygon(roiCoords)
        roiCoordsCentered = roiCoords - roiPoly.centroid.coords
        for angle in range(0,180,1):
            roiCoordsRotated = roiCoordsCentered*rotMatrix(angle)
            refPt = shapely.Point(roiCoordsRotated[0])
            yIntList = []
            for curPtCoords in roiCoordsRotated:
                curPt = shapely.Point(curPtCoords)
                if np.sign(refPt.x) != np.sign(curPt.x):
                    yIntList.append(yIntercept(refPt.x,refPt.y,curPt.x,curPt.y))
                refPt = curPt
            saveFile.write("{},{},{}\n".format(roiName,angle,max(yIntList)-min(yIntList)))
    
        
    