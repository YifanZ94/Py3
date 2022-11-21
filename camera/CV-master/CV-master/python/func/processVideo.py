'''
Name: processVideo.py

Description:

author: @katelyn98
'''

import cv2 as cv
import numpy as np
import math
import func.calculateCentroid as ccd
import func.modifOutput as mot
import func.calculateAngle as cang

def process(cap, font):
    maxLeft = 0
    maxRight = 0 
    while(1):
        _, frame = cap.read()
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        #color 1
        lowerBlue = np.array([10, 100, 100])
        upperBlue = np.array([50, 255, 255])

        #color 2
        lowerGreen = np.array([150, 75, 75])
        upperGreen = np.array([255, 200, 200])

        #gives us a binary image of black and white
        maskYellow = cv.inRange(hsv, lowerBlue, upperBlue)
        maskGreen = cv.inRange(hsv, lowerGreen, upperGreen)

        #parameters: input, threshold value (used to classify pixel values), maxVal (value to assign if pixel is more or less than thresh val)
        __, thresh = cv.threshold(maskYellow, 190, 255, cv.THRESH_BINARY)
        __, thresh2 = cv.threshold(maskGreen, 127, 255, cv.THRESH_BINARY)

        #Find contours
        contours, ___ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        contours2, ___ = cv.findContours(thresh2, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        contoursList = [contours, contours2]

        #Calculate centroid
        cx, cy, cx2, cy2, xL, yL, xR, yR = ccd.calcCentroid(contoursList, len(contoursList))
        coordList = [cx, cy, cx2, cy2, xL, yL, xR, yR]

        #draw contours and centroids
        mot.drawContoursLines(frame, contoursList, coordList, font)
        
        angleCalculated, direction = cang.angleCalculation(xL, yL, xR, yR)
        
        if angleCalculated > maxLeft:
            if direction == "Left":
                maxLeft = angleCalculated
        if angleCalculated > maxRight:
            if direction == "Right":
                maxRight = angleCalculated
        
        mot.addText(frame, angleCalculated, direction, font)

        cv.imshow("Thoracic Rotation Range of Motion", frame)
        
        k = cv.waitKey(5) & 0xff
        if k == 27:
            break

    cv.destroyAllWindows()