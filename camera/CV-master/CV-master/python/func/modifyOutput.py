import cv2 as cv

def drawContoursLines(frame, contoursList, coordsList, font):

    contours = contoursList[0]
    contours2 = contoursList[1]

    cx = coordsList[0]
    cy = coordsList[1]
    cx2 = coordsList[2]
    cy2 = coordsList[3]
    xL = coordsList[4]
    yL = coordsList[5]
    xR = coordsList[6]
    yR = coordsList[7]

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

def addText(frame, angle, direction, font):
    cv.putText(frame, str(float("{0:.2f}".format(angleCalculated))), (25,100), font, 1, (255, 255, 255), 2, cv.LINE_AA)
    cv.putText(frame, str(direction), (125,100), font, 1, (255, 255, 255), 2, cv.LINE_AA)
    cv.putText(frame, str(float("{0:.2f}".format(maxLeft))) + " MaxL", (450,100), font, 1, (255, 255, 255), 2, cv.LINE_AA)
    cv.putText(frame, str(float("{0:.2f}".format(maxRight))) + " MaxR", (450,150), font, 1, (255, 255, 255), 2, cv.LINE_AA)