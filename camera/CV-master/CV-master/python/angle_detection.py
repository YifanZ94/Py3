#From angle detection tutorial online: https://botforge.wordpress.com/2016/07/20/live-camera-based-angle-calculator-using-python-and-opencv/

#We only want to show the user the original image, they should not be seeing the res or mask

#TODO: blend final images

#import libs
import cv2
import numpy as np
import math
 
#uses distance formula to calculate distance
def distance(x1, y1, x2,y2):
    dist = math.sqrt(math.fabs(x2-x1)**2+math.fabs(y2-y1)**2)
    return dist
 
#filters for green color [origin] and returns green color [origin] position.
def findgreenOrigin(frame):

    #convert BGR to HSV
    green_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #define range of green in HSV
    #HSV = [Hue range, Saturation range, Value range]
    greenlow = np.array([37, 140, 208]) #RGB = (182, 255, 105)
    greenhi = np.array([40, 165, 189]) #RGB = (0, 255, 106)
    #Threshold in HSV image to get only green colors
    mask = cv2.inRange(green_hsv, greenlow, greenhi)
    #Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask=mask)
    #find contours of a [binary image]
    frame2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #draw the contours found on the image [video]
    cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)

    if len(contours) > 0:
        maxcontour = max(contours, key = cv2.contourArea)
 
        #All this stuff about moments and M['m10'] etc.. are just to return center coordinates
        M = cv2.moments(maxcontour)
        if M['m00'] > 0 and cv2.contourArea(maxcontour) > 1000:
            #calculation of centroid
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            return (cx, cy), True
        else:
            #(700,700), arbitrary random values that will conveniently not be displayed on screen
            return (700,700), False
    else:
        return (700,700), False

#filters for pink color [right shoulder regristration mark] and returns position.
def findpink(frame):
    
    pink = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    pinklow = np.array([132, 130, 245]) #RGB = (255, 130, 255)
    pinkhi = np.array([140, 160, 255]) #RBG = (255, 0, 191)

    mask = cv2.inRange(pink, pinklow, pinkhi)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    frame2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #draw contours on the video
    cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)

    if len(contours) > 0:
        maxcontour = max(contours, key = cv2.contourArea)

        M = cv2.moments(maxcontour)
        if M['m00'] > 0 and cv2.contourArea(maxcontour) > 1000:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            return(cx, cy), True
        else:
            return (700, 700), False
    else:
        return (700, 700), False 

cap = cv2.VideoCapture(0)

while(1):
    _, frame = cap.read()

    #get the coordinates of each objects
    (greenx, greeny), blogic = findgreenOrigin(frame)
    (pinkx, pinky), plogic = findpink(frame)

    #calculate the angle for left shoulder
    if blogic and plogic:
        #quantifies the hypotenuse of the triangle
        hypotenuse = distance((greenx, greeny), (pinkx, pinky))
        #quantifies the horizontal of the triangle
        horizontal = distance((greenx, greeny), (pinkx, greeny))
        #makes the third line of the triangle
        vertical = distance((pinkx, pinky), (pinkx, greeny))
        #calculates the angle using trigonometry
        angle = np.arcsin(vertical/hypotenuse)*180/math.pi

        #draws all 3 lines
        cv2.line(frame, (greenx, greeny), (pinkx, pinky), (0, 0, 255), 2)
        cv2.line(frame, (greenx, greeny), (pinkx, greeny), (0, 0, 255), 2)
        cv2.line(frame, (pinkx,pinky), (pinkx, greeny), (0,0,255), 2)

        #angle text
        angle_text = ""

        #Allows for calculation until 180 degrees instead of 90
        if pinky < greeny and pinkx > greenx:
            angle_text = str(int(angle))
        elif pinky < greeny and pinkx < greenx:
            angle_text = str(int(180 - angle))
        elif pinky > greeny and pinkx < greenx:
            angle_text = str(int(180 + angle))
        elif pinky > greeny and pinkx > greenx:
            angle_text = str(int(360 - angle))

        #CHANGE FONT HERE
        cv2.putText(frame, angle_text, (greenx-30, greeny), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 128, 229), 2)

    cv2.imshow('AngleCalc', frame)
    cv2.waitKey(5)

cap.release()
cv2.destroyAllWindows()
