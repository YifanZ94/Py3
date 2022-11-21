import cv2 as cv
import numpy as np

font = cv.FONT_HERSHEY_SIMPLEX

cap = cv.VideoCapture(0)

while(1):

    _, frame = cap.read()
    
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    blur = cv.GaussianBlur(hsv, (5, 5), 0)

    lowerGreen = np.array([70, 100, 100])
    upperGreen = np.array([90, 255, 255])

    maskGreen = cv.inRange(hsv, lowerGreen, upperGreen)

    kernel = np.ones((5, 5), np.uint8)
    dilate = cv.dilate(maskGreen, kernel, iterations=2)

    ret, thresh = cv.threshold(dilate, 15, 255, cv.THRESH_BINARY)

    _, contours, _ = cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

    #draw contours
    cv.drawContours(frame, contours, -1, (0, 255, 0), 3)
    cv.drawContours(thresh, contours, -1, (0, 255, 0), 3)

    if len(contours) > 0:
        #outputs a dictionary of all moments calculated like area, centroid, etc
        #TENNIS BALL 1 Centroid
        M = cv.moments(contours[0])

        if M['m00'] > 0:
            #calculation of centroid
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            #draw centroid
            centroid = cv.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
            cv.putText(frame, "Centroid", (cx - 25, cy -25), font, 1, (255, 255, 255), 2, cv.LINE_AA)

            centroid = cv.circle(thresh, (cx, cy), 5, (0, 0, 255), -1)
            cv.putText(thresh, "Centroid", (cx - 25, cy -25), font, 1, (255, 255, 255), 2, cv.LINE_AA)
            
        else:
            cx, cy = 700, 700

        #TENNIS BALL 2 Centroid
        M = cv.moments(contours[1])

        if M['m00'] > 0:
            #calculation of centroid
            cx2 = int(M['m10'] / M['m00'])
            cy2 = int(M['m01'] / M['m00'])
            #draw centroid
            centroid = cv.circle(frame, (cx2, cy2), 5, (0, 0, 255), -1)
            cv.putText(frame, "Centroid2", (cx2 - 25, cy2 -25), font, 1, (255, 255, 255), 2, cv.LINE_AA)

            centroid = cv.circle(thresh, (cx2, cy2), 5, (0, 0, 255), -1)
            cv.putText(thresh, "Centroid2", (cx2 - 25, cy2 -25), font, 1, (255, 255, 255), 2, cv.LINE_AA)
            
        else:
            cx2, cy2 = 700, 700

    else:
        cx, cy = 700, 700
        cx2, cy2 = 700, 700

    #draw line from centroids
    cv.line(frame, (cx, cy), (cx2, cy2), (255, 0 , 0), 5)

    cv.line(thresh, (cx, cy), (cx2, cy2), (255, 0 , 0), 5)

    #draw a horizontal line across the center of the screen to represent bar
    cv.line(frame, (0, 250), (500, 250), (140, 50, 80), 5)

    cv.line(thresh, (0, 250), (500, 250), (140, 50, 80), 5)

    cv.imshow("Thresh", thresh)
    cv.imshow("Dilate", dilate)
    cv.imshow("Frame", frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()


