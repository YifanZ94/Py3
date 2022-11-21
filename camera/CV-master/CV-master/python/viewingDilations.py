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

    cv.imshow("Thresh", thresh)
    cv.imshow("Dilate", dilate)
    cv.imshow("Frame", frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()