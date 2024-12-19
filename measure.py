import os
import zipfile
import roifile
from numpy import matrix,sin,cos,degrees,sign
from numpy import append as npappend
import shapely

zipFilePath=r"C:\Users\jonme\Documents\School Work\Research - Bowman Lab\wagonWheelMeasurer\ignore\25C-winA-preEDS-1.zip"
tempStoragePath=r"C:\Users\jonme\Documents\School Work\Research - Bowman Lab\wagonWheelMeasurer\ignore\temporaryRoiStorage"
saveFilePath=r"C:\Users\jonme\Documents\School Work\Research - Bowman Lab\wagonWheelMeasurer\ignore\25C-winA-preEDS-1.txt"

def rotMatrix(theta):
    # returns a numpy rotation matrix at the given angle (radians)
    theta = degrees(theta)
    return matrix([[cos(theta),-sin(theta)],[sin(theta),cos(theta)]])

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
    #coordList.append(roifile.ImagejRoi.fromfile(file).coordinates().tolist())
    #^adding to      ^creating an object from         ^extracting the ^converting the numpy list
    #the list        the ROI file                     coordinates out  into a python list so it's
    #                                                 of that object   MATLAB readable

for file in fileNames:
    os.remove(file)

# with open("readme.txt","w") as readme:
#     readme.write("groups of roi files are stored in a .zip file.\nThis script needs a temporary place to store the unzipped ROIs while it runs.\nBecause this is a folder for temporary files, the contents are deleted every time you run measure.py\nDO NOT STORE ANYTHING IN THIS FOLDER. LET THE PROGRAM HANDLE IT.")

with open(saveFilePath,"a") as saveFile:
    saveFile.write("ROI Name,Angle,Diameter(px)\n")
    for roiCoords,roiName in zip(roiList,fileNames):
        roiCoords = npappend(roiCoords,[roiCoords[0]], axis=0)
        roiPoly = shapely.Polygon(roiCoords)
        roiCoordsCentered = roiCoords - roiPoly.centroid.coords
        for angle in range(0,180,1):
            roiCoordsRotated = roiCoordsCentered*rotMatrix(angle)
            refPt = shapely.Point(roiCoordsRotated[0])
            yIntList = []
            for curPtCoords in roiCoordsRotated:
                curPt = shapely.Point(curPtCoords)
                if sign(refPt.x) != sign(curPt.x):
                    yIntList.append(yIntercept(refPt.x,refPt.y,curPt.x,curPt.y))
                refPt = curPt
            saveFile.write("{},{},{}\n".format(roiName,angle,max(yIntList)-min(yIntList)))
    
        
    