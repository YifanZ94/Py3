import numpy as np
import cv2 as cv
import math
cap = cv.VideoCapture(0)
font = cv.FONT_HERSHEY_SIMPLEX
maxLeft = 0
maxRight = 0
#First we get two sets of (x,y) coordinates, Left Ball and Right Ball
#We have: xL, yL, xR, yR
#Choose Coordinates to Test
#xL=1
#yL=1
#xR=-1
#yR=1
#Angle Calculation
def angleCalculation(xL, yL, xR, yR):
    
    #determine if Left or Right
    if yR>yL: #left
        direction = "Left"
        if xL>xR: #0-90 
            #CASE 1L: angle is between 0 and 90
            m1 = (yR-yL)/(xL-xR) #slope
            rad = math.atan(m1)
            angle = rad*180/math.pi
            case = "1L"
        elif xL<xR: #>90
            #CASE 2L: angle is greater than 90
            m1 = (yR-yL)/(xL-xR) #slope
            rad = math.atan(m1)
            angle = 180 + rad*180/math.pi
            case = "2L"
        else: 
            #angle is exactly 90
            angle = 90   
    elif yR<yL: #right
        direction = "Right"
        if xL>xR: #0-90
            #CASE 1R: angle is between 0 and 90
            m1 = (yR-yL)/(xL-xR) #slope
            rad = math.atan(m1)
            angle = -rad*180/math.pi
            case = "1R"
        elif xL<xR: #>90
            #CASE 2R: angle is greater than 90
            m1 = (yR-yL)/(xL-xR) #slope
            rad = math.atan(m1)
            angle = 180 - rad*180/math.pi
            case = "2R"
        else:
            #angle is exactly 90
            angle = 90
    else: #horizontal
        angle = 0
        direction = "Horizontal"
    
    return angle, direction
def process():
    while(1):
        _, frame = cap.read()
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        """ lowerGreen = np.array([5, 50, 50])
        upperGreen = np.array([25, 255, 255]) """
        #lowerPink = np.array([140, 100, 100])
        #upperPink = np.array([160, 255, 255])
        # lowerYellow = np.array([159, 39, 125])
        # upperYellow = np.array([174, 130, 255])
        lowerBlue = np.array([10, 100, 100])
        upperBlue = np.array([50, 255, 255])
        
        # lowerGreen = np.array([25, 72, 121])
        # upperGreen = np.array([43, 250, 255])
        lowerGreen = np.array([150, 75, 75])
        upperGreen = np.array([255, 200, 200])
        #gives us a binary image of black and white
        maskYellow = cv.inRange(hsv, lowerBlue, upperBlue)
        maskGreen = cv.inRange(hsv, lowerGreen, upperGreen)
        #parameters: input, threshold value (used to classify pixel values), maxVal (value to assign if pixel is more or less than thresh val)
        __, thresh = cv.threshold(maskYellow, 190, 255, cv.THRESH_BINARY)
        __, thresh2 = cv.threshold(maskGreen, 127, 255, cv.THRESH_BINARY)
        contours, ___ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        contours2, ___ = cv.findContours(thresh2, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            maxcontour = max(contours, key = cv.contourArea)
            #outputs a dictionary of all moments calculated like area, centroid, etc
            M = cv.moments(maxcontour)
            if M['m00'] > 0 and cv.contourArea(maxcontour) > 100:
                #calculation of centroid
                cx = int(M['m10'] / M['m00'])
                xL = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                yL = int(M['m01'] / M['m00'])
            else:
                cx, cy = 10000, 250
                xL, yL = 10000, 250
        else:
            cx, cy = 10000, 250
            xL, yL = 10000, 250
        if len(contours2) > 0:
            maxcontour = max(contours2, key = cv.contourArea)
            #outputs a dictionary of all moments calculated like area, centroid, etc
            M = cv.moments(maxcontour)
            if M['m00'] > 0 and cv.contourArea(maxcontour) > 100:
                #calculation of centroid
                cx2 = int(M['m10'] / M['m00'])
                xR = int(M['m10'] / M['m00'])
                cy2 = int(M['m01'] / M['m00'])
                yR = int(M['m01'] / M['m00'])
            else:
                cx2, cy2 = -10000, 250
                xR, yR = -10000, 250
        else:
            cx2, cy2 = -10000, 250
            xR, yR = -10000, 250
        #draw contours
        cv.drawContours(frame, contours, -1, (0, 255, 0), 3)
        cv.drawContours(frame, contours2, -1, (0, 255, 0), 3)
        #draw centroid
        cv.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
        cv.putText(frame, "L", (cx - 25, cy -25), font, 1, (255, 255, 255), 2, cv.LINE_AA)
        cv.circle(frame, (cx2, cy2), 5, (0, 0, 255), -1)
        cv.putText(frame, "R", (cx2 - 25, cy2 -25), font, 1, (255, 255, 255), 2, cv.LINE_AA)
        #draw line from centroid
        cv.line(frame, (cx, cy), (cx2, cy2), (255, 0 , 0), 5)
        
        angleCalculated, direction = angleCalculation(xL, yL, xR, yR)
        global maxLeft
        global maxRight
        if angleCalculated > maxLeft:
            if direction == "Left":
                maxLeft = angleCalculated
        if angleCalculated > maxRight:
            if direction == "Right":
                maxRight = angleCalculated
        
        
        cv.putText(frame, str(float("{0:.2f}".format(angleCalculated))), (25,100), font, 1, (255, 255, 255), 2, cv.LINE_AA)
        cv.putText(frame, str(direction), (125,100), font, 1, (255, 255, 255), 2, cv.LINE_AA)
        cv.putText(frame, str(float("{0:.2f}".format(maxLeft))) + " MaxL", (450,100), font, 1, (255, 255, 255), 2, cv.LINE_AA)
        cv.putText(frame, str(float("{0:.2f}".format(maxRight))) + " MaxR", (450,150), font, 1, (255, 255, 255), 2, cv.LINE_AA)
        print(angleCalculated, direction)
        print(xL, " ", yL, " ",xR," ", yR)
        cv.imshow("centroid & line", frame)
        
        k = cv.waitKey(5) & 0xff
        if k == 27:
            break
    cv.destroyAllWindows()
process()