import numpy as np
import cv2 as cv

#grab the video from the Pi Camera
cap = cv.VideoCapture(0)

#set the font
font = cv.FONT_HERSHEY_SIMPLEX

#for every frame, do what is in the while loop
while(1):

    _, frame = cap.read()

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    lowerPink = np.array([10, 100, 100])
    upperPink = np.array([50, 255, 255])

    #gives us a binary image of black and white
    maskPink = cv.inRange(hsv, lowerPink, upperPink)

    #parameters: input, threshold value (used to classify pixel values), maxVal (value to assign if pixel is more or less than thresh val)
    ret, thresh = cv.threshold(maskPink, 127, 255, cv.THRESH_BINARY)

    #get the boundary, outline of the object we are detecting
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    #if we have contours 
    if len(contours) > 0:
        maxcontour = max(contours, key = cv.contourArea)

        #outputs a dictionary of all moments calculated like area, centroid, etc
        M = cv.moments(maxcontour)

        if M['m00'] > 0 and cv.contourArea(maxcontour) > 1000:
            #calculation of centroid
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
        else:
            #if there are no moments, set their coordinates to be someplace off the screen
            # 0,0 is the top right coorner, so 700,700 would be bottom right corner 
            # if the camera resolution is smaller than 700,700 then this point will be out of view
            cx, cy = 700, 700
    else:
        cx, cy = 700, 700

    #draw contours
    img = cv.drawContours(frame, contours, -1, (0, 255, 0), 3)

    #draw centroid
    centroid = cv.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
    cv.putText(frame, "Centroid", (cx - 25, cy -25), font, 1, (255, 255, 255), 2, cv.LINE_AA)

    #draw line from centroid
    line = cv.line(frame, (cx, cy), ((cx + 400), (cy + 400)), (255, 0 , 0), 5)

    cv.imshow("centroid & line", frame)

    k = cv.waitKey(5) & 0xff

    if k == 27:
        break

cv.destroyAllWindows()
