'''
Name: main.py

Description: 

author: @katelyn98
'''
import cv2 as cv
import func.processVideo as ppv

font = cv.FONT_HERSHEY_SIMPLEX

if __name__ == '__main__':
    cap = cv.VideoCapture(0)
    font = cv.FONT_HERSHEY_SIMPLEX

    ppv.process(cap, font)