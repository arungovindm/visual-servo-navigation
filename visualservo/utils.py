import numpy as np
import cv2
from visualservo.Classes import *

def getTransform(pose,f,scale_factor,w,h):
    rotX = (pose.rotx - 90)*np.pi/180
    rotY = (pose.roty - 90)*np.pi/180
    rotZ = (pose.rotz - 90)*np.pi/180

    #Projection 2D -> 3D matrix
    A1= np.matrix([[1, 0, -w/2],
                   [0, 1, -h/2],
                   [0, 0, 0  ],
                   [0, 0, 1   ]])

    # Rotation matrices around the X,Y,Z axis
    RX = np.matrix([[1,           0,            0, 0],
                    [0,np.cos(rotX),-np.sin(rotX), 0],
                    [0,np.sin(rotX),np.cos(rotX) , 0],
                    [0,           0,            0, 1]])

    RY = np.matrix([[ np.cos(rotY), 0, np.sin(rotY), 0],
                    [            0, 1,            0, 0],
                    [ -np.sin(rotY), 0, np.cos(rotY), 0],
                    [            0, 0,            0, 1]])

    RZ = np.matrix([[ np.cos(rotZ), -np.sin(rotZ), 0, 0],
                    [ np.sin(rotZ), np.cos(rotZ), 0, 0],
                    [            0,            0, 1, 0],
                    [            0,            0, 0, 1]])

    #Composed rotation matrix with (RX,RY,RZ)
    R = RX * RY * RZ

    #Translation matrix on the Z axis change dist will change the height
    T = np.matrix([[scale_factor,0,0,0.56*pose.xDist],
                   [0,scale_factor,0,0.56*pose.yDist],
                   [0,0,scale_factor,pose.zDist],
                   [0,0,0,scale_factor]])

    #Camera Intrisecs matrix 3D -> 2D
    A2= np.matrix([[f, 0, w/2,0],
                   [0, f, h/2,0],
                   [0, 0,   1,0]])

    # Final and overall transformation matrix
    H = A2 * (T * (R * A1))
    return H
# ==================================================================#
# function that computes the transformation matrix from the relative
# pose between the two viewpoints
# ==================================================================#
def getCorners(transform,w,h):
    default = Corners(w,h)
    temp = np.matrix([[default.tl.x],[default.tl.y],[1]])
    temp = transform * temp/1000
    default.tl.x = int(temp.item(0,0)/temp.item(2,0))
    default.tl.y = int(temp.item(1,0)/temp.item(2,0))
    

    temp = np.matrix([[default.tr.x],[default.tr.y],[1]])
    temp = transform * temp/1000
    default.tr.x = int(temp.item(0,0)/temp.item(2,0))
    default.tr.y = int(temp.item(1,0)/temp.item(2,0))
 
    temp = np.matrix([[default.bl.x],[default.bl.y],[1]])
    temp = transform * temp/1000
    default.bl.x = int(temp.item(0,0)/temp.item(2,0))
    default.bl.y = int(temp.item(1,0)/temp.item(2,0))

    temp = np.matrix([[default.br.x],[default.br.y],[1]])
    temp = transform * temp
    default.br.x = int(temp.item(0,0)/temp.item(2,0))
    default.br.y = int(temp.item(1,0)/temp.item(2,0))
   
    return default
#==================================================================#
#function that finds the coordinates of the bounding box of the war-
#ped image.

#the two images i.e, ground truth and image transfer are cropped be-
#tween these corners and difference is calculated by getDistance
#==================================================================#
def getDistance(target,pred,corners):
    
    target = target[corners.tl.y:corners.bl.y, corners.tl.x:corners.tr.x].copy()
    pred = pred[corners.tl.y:corners.bl.y, corners.tl.x:corners.tr.x].copy()
    cv2.imwrite('/home/arun/cropped_diff.jpg',target-pred)
    cv2.imwrite('/home/arun/cropped_target.jpg',target)
    cv2.imwrite('/home/arun/cropped_pred.jpg',pred)
    h,w =target.shape[:2]
    target = np.array(target).reshape((w*h))
    pred = np.array(pred).reshape((w*h))
    cos = (target*pred).sum()/(len(pred)*len(target))
    print("cosine:={}\tNSAD:={}\tSAD:={}".format(cos,abs(target-pred).sum()/(w*h),abs(target-pred).sum()))
    return abs(target-pred).sum()/(w*h)
#==================================================================#
# function that computes difference between warped image and ground
# truth inside the bounding box computed by getCorners
# =================================================================#
def len(a):
    return np.linalg.norm(a)
