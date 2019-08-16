import numpy as np
from visualservo.Classes import *
from visualservo.utils import *
def driverCode(args,src,ground_truth):

    #define camera instrinsic parameters
    f = 241.42682359130833*1.755
    scale_factor = 1

    pose = sixDOFRelativePose(args,f)

    dst = np.ndarray(shape=src.shape,dtype=src.dtype)
    h , w = src.shape[:2]
    H = getTransform(pose,f,scale_factor,w,h)
    corners = getCorners(H,w,h)
    cv2.warpPerspective(src, H, (w, h), dst, cv2.INTER_CUBIC)
 
    
    diff = getDistance(ground_truth, dst, corners)

    wndname1 = "Ground Truth:"
    wndname2 = "WarpPerspective: "
    cv2.namedWindow(wndname1, 1)
    cv2.namedWindow(wndname2, 1)
    cv2.imshow(wndname1, ground_truth)
    cv2.imshow(wndname2, dst)
    cv2.waitKey(0)
