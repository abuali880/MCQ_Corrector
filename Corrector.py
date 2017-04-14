import numpy as np
import argparse
import imutils
import cv2
import os
import math
#import cv2.cv as cv

name = "output"
directory = "/home/mostafa/TrainData"
thresh = 150
maxValue = 255
kernel = np.ones((10,10),np.uint8)

def rotate(image, angle,cX,cY):
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    #(cX, cY) = (w // 2, h // 2)
    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
    # perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH))
for filename in os.listdir(directory):
    if filename.endswith(".png"): 
        flag = True
        image = cv2.imread(os.path.join(directory, filename),0)
        img = image
        img = img[1400:1800, 0:1500]
        img = cv2.medianBlur(img,5)
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        th, img2 = cv2.threshold(img, thresh, maxValue, cv2.THRESH_BINARY_INV)
        img2 = cv2.bitwise_not(img2)
        cimg = cv2.cvtColor(img2,cv2.COLOR_GRAY2BGR)
        circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=0,maxRadius=0)
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            if flag:
        		# first center coordinates
                x1=i[0]
                y1=i[1]
                flag = False
            else:
                #second center coordinates
                x2=i[0]
                y2=i[1]
                pass
        	pass
        if x1 > x2:
            tmp1 = x2
            tmp2 = y2
            x2 = x1
            y2 = y1
            x1 = tmp1
            y1 = tmp2
            pass
        print(x1,y1)    
        delta_x = float(x2-x1)
        delta_y = float(y2)-float(y1)
        rads = math.atan2(delta_y, delta_x)
        angle = math.degrees(rads) 
        print(angle)
        image = imutils.rotate_bound(image, angle=-angle)
        image = imutils.translate(image,226-x1 , 140-y1)
        image = image[700:1450, 100:1200]
        image1 = image[0:1500, 0:350]
        image2= image[0:1500, 350:700]
        image3 = image[0:1500, 700:1050]
        cv2.namedWindow(os.path.join(directory, filename),cv2.WINDOW_NORMAL)
        cv2.resizeWindow(os.path.join(directory, filename), 700,700)
        cv2.imshow(os.path.join(directory, filename),image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        continue
    else:
        continue
        pass
