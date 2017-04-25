import numpy as np
import argparse
import imutils
import cv2
import os
import math
#import cv2.cv as cv
def isExis(k,Xaxis):
    tmp = []
    for x in xrange(0,len(Xaxis)):
        if k[0] < Xaxis[x]+7 and k[0] > Xaxis[x]-7:
            #Xaxis.remove(Xaxis[x])
            continue
        else:
            tmp.append(Xaxis[x])
        pass
    return tmp
    pass

def predictCircles(l,Xaxis):
    Ox = Xaxis
    if(len(l) != 4):
        for x in xrange(0,len(l)):
        	Xaxis = isExis(l[x],Xaxis)
        pass
        for y in xrange(0, len(Xaxis)):
            l.append(np.array([Xaxis[y], l[0][1], 11]))
    l = sorted(l, key=lambda x: x[0])
    return l , Ox
    pass


name = "output"
directory = "/home/mostafa/TrainData"
thresh = 150
maxValue = 255
kernel = np.ones((10,10),np.uint8)

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
        delta_x = float(x2-x1)
        delta_y = float(y2)-float(y1)
        rads = math.atan2(delta_y, delta_x)
        angle = math.degrees(rads)
        thresh = 220
        image = imutils.rotate_bound(image, angle=-angle)
        image = imutils.translate(image,226-x1 , 140-y1)
        image = image[700:1450, 100:1200]
        th, image = cv2.threshold(image, thresh, maxValue, cv2.THRESH_BINARY)
        image1 = image[0:1500, 0:350]
        image2= image[0:1500, 350:700]
        image3 = image[0:1500, 700:1050]
        images = [image1,image2,image3]
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(10,10))
        for xx in xrange(0,3):
            blurred = cv2.GaussianBlur(images[xx], (5, 5), 0)
            circles = cv2.HoughCircles(blurred,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=8,maxRadius=14)
            circles = np.round(circles[0, :]).astype("int")
            images[xx] = cv2.cvtColor(images[xx], cv2.COLOR_GRAY2BGR)
            Ccircles = np.zeros(circles.shape[1])
            SortedCircles = sorted(circles, key=lambda x: x[1])
            #print SortedCircles
            Ques = {}
            k = 1
            pre = 0
            Ques[k] = []
            flag = True
            Xaxis = []
            for i,val in enumerate(SortedCircles):
                if i==0:
                    Ques[k].append(val)
                    pre = val[1]
                    continue
                else:
                    if ((val[1] - pre) < 7):
                        Ques[k].append(val)
                        continue
                    else:
                        # if k == 15:
                        #     break
                        #     pass
                        if len(Ques[k]) == 4 and flag:
                            Xaxis = [Ques[k][0][0],Ques[k][1][0],Ques[k][2][0],Ques[k][3][0]]
                            Xaxis = sorted(Xaxis)
                            #print Xaxis
                            flag = False
                            pass
                        k+=1
                        Ques[k]=[]
                        Ques[k].append(val)
                    pre = val[1]
                pass
            for k , v in Ques.items():
                v , Xaxis = predictCircles(v,Xaxis)
                if len(v) != 4:
                	Ques.pop(k)
                	pass
                #print k , v
            for i in Ques.values():
                for x in xrange(0,len(i)):
                    # draw the outer circle
                    cv2.circle(images[xx],(i[x][0],i[x][1]),i[x][2],(0,255,0),2)
                    # draw the center of the circle
                    cv2.circle(images[xx],(i[x][0],i[x][1]),2,(0,0,255),3)
                    pass
            # for i in circles:
	           #  #draw the outer circle
	           # cv2.circle(images[xx],(i[0],i[1]),i[2],(0,255,0),2)
	           #  #draw the center of the circle
	           # cv2.circle(images[xx],(i[0],i[1]),2,(0,0,255),3)
	           # pass
            cv2.namedWindow(os.path.join(directory, filename),cv2.WINDOW_AUTOSIZE)
            #cv2.resizeWindow(os.path.join(directory, filename), 700,700)
            cv2.imshow(os.path.join(directory, filename),np.hstack([images[xx]]))
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        continue
    else:
        continue
        pass
