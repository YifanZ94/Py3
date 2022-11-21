import cv2 as cv
import numpy as np

font = cv.FONT_HERSHEY_SIMPLEX

cap = cv.VideoCapture(0)

while(1):

    _, frame = cap.read()

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    blur = cv.GaussianBlur(hsv, (5, 5), 0)

    lowerGreen = np.array([30, 100, 100])
    upperGreen = np.array([45, 225, 225])

    #gives us a binary image of black and white
    mask = cv.inRange(hsv, lowerGreen, upperGreen)
    #parameters: input, threshold value (used to classify pixel values), maxVal (value to assign if pixel is more or less than thresh val)

    kernel = np.ones((5, 5), np.uint8)
    dilate = cv.dilate(mask, kernel, iterations=2)

    ret, thresh = cv.threshold(dilate, 15, 275, cv.THRESH_BINARY)

    res = cv.bitwise_and(frame, frame, mask= thresh)
    #Find the contours
    #parameters: input, contour retrieval mode, contour approximation method
    #outputs an image, contours (a list of all the contours in the image),and hierarchy
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    #parameters: input, contours to be passed in, draw all contours (-1) or index to a specific one, color, thickness
    img = cv.drawContours(frame, contours, -1, (0, 255, 0), 3)

    if len(contours) > 0:
        #outputs a dictionary of all moments calculated like area, centroid, etc
        
        #TENNIS BALL 1 Centroid
        M = cv.moments(contours[0])

        if M['m00'] > 0:
            #calculation of centroid
            cx = int(M['m10'] / M['m00'])
            xL = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            yL = int(M['m01'] / M['m00'])
            #draw centroid
            centroid = cv.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
            cv.putText(frame, "Centroid", (cx - 25, cy -25), font, 1, (255, 255, 255), 2, cv.LINE_AA)
            
        else:
            #draw centroids off the screen
            cx, cy = 700, 700
            xL, yL = 700, 700

        if len(contours) > 1:

            #TENNIS BALL 2 Centroid
            M = cv.moments(contours[1])

            if M['m00'] > 0:
            
                cx2 = int(M['m10'] / M['m00'])
                xR = int(M['m10'] / M['m00'])
                cy2 = int(M['m01'] / M['m00'])
                yR = int(M['m01'] / M['m00'])
                centroid = cv.circle(frame, (cx2, cy2), 5, (0, 0, 255), -1)
                cv.putText(frame, "Centroid2", (cx2 - 25, cy2 -25), font, 1, (255, 255, 255), 2, cv.LINE_AA)
                
            else:
                cx2, cy2 = 700, 700
                xR, yR = 700, 700
        else: 
            cx2, cy2 = 700, 700
            xR, yR = 700, 700
    else:
        cx, cy = 700, 700
        xL, yL, xR, yR = 700, 700, 700, 700
        cx2, cy2 = 700, 700

    cv.line(frame, (cx, cy), (cx2, cy2), (255, 0 , 0), 5)

    center_x1 = 125
    center_x2 = 525
    center_y = 250

    cv.line(frame, (center_x1, center_y), (center_x2, center_y), (130, 40, 230), 3)    
    

    #cv.imshow("Thresh", blur)
    #cv.imshow("HSV", hsv)
    #cv.imshow("contours", thresh)
    cv.imshow("Frame", mask)
    cv.imshow("res", res)
    cv.imshow("frame", frame)
    #cv.imshow("Contours", img)

    k = cv.waitKey(5) & 0xff

    if k == 27:
        break

cv.destroyAllWindows()