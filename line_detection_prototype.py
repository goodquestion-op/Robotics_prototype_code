# You may run into issues installing pytesseract, this is because python wants you to install things into virtual environments
# For our usecase, venv aren't super useful as we are only making one project at a time, so use the flags below:
# sudo pip3 install pytesseract --break-system-packages
# https://nanonets.com/blog/ocr-with-tesseract/
from PIL import Image
#import pytesseract
import cv2
import os, sys, inspect #For dynamic filepaths
import numpy as np;
import serial
import time
import math




cam = cv2.VideoCapture(0)

while True:
    check, frame = cam.read()

    image = cv2.resize(frame,(320,240))
    # Resize

    # Greyscale
    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    

    # Threshold         120 is threshold, 255 is what we assign if it is below this
    _, thresh = cv2.threshold(image, 70, 255, cv2.THRESH_BINARY)

    # Canny
    #image = cv2.Canny(image, 50,200,)
    


    # #hough lines
    dst = cv2.Canny(grey, 50, 200, None,3)

    cdst = cv2.cvtColor(dst,cv2.COLOR_GRAY2BGR)
    cdstP = np.copy(cdst)

    lines = cv2.HoughLines(dst,1,np.pi/180,150,None,0,20)
    if lines is not None:
        for i in range(0,len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000*(-b)),int(y0 + 1000*(a)))
            pt2 = (int(x0 - 1000*(-b)),int(y0 - 1000*(a)))

            cv2.line(cdst, pt1 ,pt2, (0,0,255), 3, cv2.LINE_AA)

    linesP = cv2.HoughLinesP(dst,1,np.pi/180,50,None,100,20)

    if linesP is not None:
        for i in range(0,len(linesP)):
            l = linesP[i][0]
            cv2.line(cdstP, (l[0],l[1]),(l[2],l[3]),(255,255,255),3,cv2.LINE_AA)

    cdstPg = cv2.cvtColor(cdstP, cv2.COLOR_BGR2GRAY)
    _, cdstPBI = cv2.threshold(cdstPg, 70, 255, cv2.THRESH_BINARY)
    

    PH = cdstP

    cv2.imshow('image', image)
    cv2.imshow("Detected Lines (in red) - Standard Hough Line Transform", cdst) 
    
    
    cv2.imshow("Detected Lines (in red) - probabilistic Line Transform", PH)

    cv2.imwrite("image_box_text.jpg",PH)

    key = cv2.waitKey(1)
    if key == 27:
        break
      


cam.release()
cv2.destroyAllWindows()
# Resize
#image = cv2.resize(image, (320, 120))

# Greyscale
#image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Threshold         120 is threshold, 255 is what we assign if it is below this
#_, image = cv2.threshold(image, 70, 255, cv2.THRESH_BINARY)

# Canny
#image = cv2.Canny(image, 30,200)

# Countours (needs canny)
#contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
#print("Number of Contours Found = " + str(len(contours)))
#image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
#cv2.drawContours(image, contours, -1, (255,0,0),2) #

