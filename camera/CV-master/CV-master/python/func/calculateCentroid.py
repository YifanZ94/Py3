import cv2 as cv
import numpy as np
import math

areaVal1 = 10000
areaVal2 = 250
negVal1 = -10000

def calcCentroid(contoursList, numContours):

    if numContours == 2:
        contours = contoursList[0]
        contours2 = contoursList[1]

        cx, cy, cx2, cy2, xL, yL, xR, yR = twoCentroid(contours, contours2)
    #else:
        #implement to only calculate one centroid


def twoCentroid(contours, contours2):
    cx, cy = areaVal1, areaVal2
    xL, yL = areaVal1, areaVal2
    cx2, cy2 = negVal1, areaVal2
    xR, yR = negVal1, areaVal2

    if len(contours) > 0:
            #outputs a dictionary of all moments calculated like area, centroid, etc
            M, maxcontour = findMoments(contours)
            #calculate centroid
            cx, xL, cy, yL = centroidCoords(M, maxcontour, False)

    if len(contours2) > 0:
        #outputs a dictionary of all moments calculated like area, centroid, etc
        M, maxcontour = findMoments(contours2)
        #calculate centroid
        cx2, xR, cy2, yR = centroidCoords(M, maxcontour, True)

    return cx, cy, cx2, cy2, xL, yL, xR, yR
        

def findMoments(contours):
    maxcontour = max(contours, key = cv.contourArea)
    return cv.moments(maxcontour), maxcontour

def centroidCoords(M, maxcontour, neg):
    if M['m00'] > 0 and cv.contourArea(maxcontour) > 100:
        #calculation of centroid
        cx = int(M['m10'] / M['m00'])
        x = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        y = int(M['m01'] / M['m00'])
    else:
        if neg == False:
            cx, cy = areaVal1, areaVal2
            x, y = areaVal1, areaVal2
        else:
            cx, cy = negVal1, areaVal2
            x, y = negVal1, areaVal2

    return cx, x, cy, y