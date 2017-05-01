import numpy as np
import argparse
import imutils
import cv2
import os
import math
import operator
#import cv2.cv as cv
def RemoveFoundX(k,Xaxis):
    tmp = []
    for x in xrange(0,len(Xaxis)):
        if k[0] < Xaxis[x]+15 and k[0] > Xaxis[x]-15:
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
        	Xaxis = RemoveFoundX(l[x],Xaxis)
        pass
        for y in xrange(0, len(Xaxis)):
            l.append(np.array([Xaxis[y], l[0][1], 11]))
    l = sorted(l, key=lambda x: x[0])
    return l , Ox
    pass

def isEx(x,Xaxis):
	flag = False
	for f in Xaxis:
		if x < f+15 and x > f-15:
			flag = True
		pass
	return flag
	pass
def ConstructXaxis(Xaxis,Ques):
	for x in Ques:
		if not isEx(x[0],Xaxis):
			Xaxis.append(x[0])
			pass
		pass
	return Xaxis
	pass


ModelaAnswer = {
	1 : 1,
	2 : 2,
	3 : 0,
	4 : 0,
	5 : 3,
	6 : 0,
	7 : 2,
	8 : 2,
	9 : 0,
	10 : 2,
	11 : 0,
	12 : 1,
	13 : 2,
	14 : 2,
	15 : 1,
	16 : 0,
	17 : 3,
	18 : 1,
	19 : 2,
	20 : 1,
	21 : 3,
	22 : 2,
	23 : 3,
	24 : 1,
	25 : 3,
	26 : 2,
	27 : 3,
	28 : 3,
	29 : 1,
	30 : 2,
	31 : 1,
	32 : 1,
	33 : 3,
	34 : 2,
	35 : 1,
	36 : 2,
	37 : 1,
	38 : 2,
	39 : 2,
	40 : 0,
	41 : 1,
	42 : 1,
	43 : 2,
	44 : 2,
	45 : 1,
}


def run(Dir,name,sss=0):
    thresh = 150
    maxValue = 255
    show = sss
    kernel = np.ones((10,10),np.uint8)
    f = open("result.csv","a")
    direct = Dir+name
    correct = 0
    flag = True
    image = cv2.imread(direct,0)
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
    thresh = 210
    image = imutils.rotate_bound(image, angle=-angle)
    image = imutils.translate(image,226-x1 , 140-y1)
    image = image[750:1450, 100:1200]
    imagess = cv2.medianBlur(image,5)
    th, imaged = cv2.threshold(imagess, 150, maxValue, cv2.THRESH_BINARY)
    #th = image
    imaged1 = imaged[0:1500, 100:350]
    imaged2= imaged[0:1500, 350:700]
    imaged3 = imaged[0:1500, 700:1050]
    imageds = [imaged1,imaged2,imaged3]
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15,15))
    
    trialll = cv2.morphologyEx(imaged, cv2.MORPH_CLOSE, kernel)
    image = cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,23,1)
    image = cv2.medianBlur(image,3)
    #image = cv2.bitwise_and(image,trialll)
    image1 = image[0:1500, 100:350]
    image2= image[0:1500, 350:700]
    image3 = image[0:1500, 700:1050]
    images = [image1,image2,image3]
    kernel = cv2.getStructuringElement(cv2.MORPH_ERODE,(5,5))
    image = cv2.morphologyEx(image, cv2.MORPH_ERODE, kernel)
    
    FinalCircles = {}
    offset2 = 0
    for xx in xrange(0,3):
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(1,1))
        hel = cv2.morphologyEx(imageds[xx], cv2.MORPH_CLOSE, kernel)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15,15))
        whitePage = 255 * np.ones((images[xx].shape),np.uint8) #cv2.cv.CreateImage((images[xx][0],images[xx][1]),8,3) 
        whitePage2 = 255 * np.ones((images[xx].shape),np.uint8)
        mask = whitePage
        # cv2.namedWindow("White",cv2.WINDOW_AUTOSIZE)
        # cv2.moveWindow("White", 0, 0)
        # cv2.imshow("White",whitePage)
        blurred = cv2.GaussianBlur(images[xx], (5, 5), 0)
        circles = cv2.HoughCircles(blurred,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=8,maxRadius=14)
        circles = np.round(circles[0, :]).astype("int")
        #images[xx] = cv2.cvtColor(images[xx], cv2.COLOR_GRAY2BGR)
        Ccircles = np.zeros(circles.shape[1])
        SortedCircles = sorted(circles, key=lambda x: x[1])
        #print SortedCircles
        Ques = {}
        offset = 1
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
                    if len(Xaxis) < 4 and k != 1:
                    	s = Ques[k]
                        if(len(s) > 4):
                            s = sorted(s, key=lambda x: x[0])
                            s = s[len(s)-4:len(s)]
                    	Xaxis = ConstructXaxis(Xaxis,s)
                    	pass
                    # if len(Ques[k]) == 4 and flag:
                    #     Xaxis = [Ques[k][0][0],Ques[k][1][0],Ques[k][2][0],Ques[k][3][0]]
                    #     Xaxis = sorted(Xaxis)
                    #     #print Xaxis
                    #     flag = False
                    #     pass
                    k+=1
                    Ques[k]=[]
                    Ques[k].append(val)
                pre = val[1]
            pass
        if show == 1:
            print Xaxis
        if show == 1:
            for k,v in Ques.items():
                for x in xrange(1,len(v)):
                    cv2.circle(images[xx],(v[x][0],v[x][1]),v[x][2],(0,255,0),2)
                print k , v
                pass
        for k , v in Ques.items():
            v , Xaxis = predictCircles(v,Xaxis)
            if len(v) != 4:
            	Ques.pop(k)
            else:
            	FinalCircles[offset] = v
            	offset += 1
            	pass                
            # if show == 1:
            # 	print k , v[0] , v[1] ,v[2] ,v[3]
        # for k,v in FinalCircles.items():
        #     print k , v
        #     pass
        for k,v in FinalCircles.items():
            for x in xrange(0,len(v)):
                cv2.circle(whitePage2,(v[x][0],v[x][1]),5,(0,0,255),-1)
            pass
        hel = cv2.bitwise_or(hel,whitePage2)
        hel = cv2.morphologyEx(hel, cv2.MORPH_ERODE, kernel)
        images[xx] = cv2.bitwise_and(images[xx],hel)
        for k,v in FinalCircles.items():
            # if show == 1:
            #     print k,v
    		Question = []
    		doubled = False
    		for x in xrange(0,len(v)):
    			if ModelaAnswer[k+offset2] == x:
    				cv2.circle(images[xx],(v[x][0],v[x][1]),v[x][2]+5,(0,255,0),2)
    				G = 255
    				B = 0
    			else:
    				G = 0
    				B = 255
    				pass
    			images[xx] = cv2.cvtColor(images[xx], cv2.COLOR_GRAY2BGR)
    			#cv2.circle(images[xx],(v[x][0],v[x][1]),v[x][2]+10,(0,255,0),2)# draw the outer circle
    			#cv2.circle(images[xx],(v[x][0],v[x][1]),v[x][2],(0,G,B),2)
    			#draw the center of the circle
    			#cv2.circle(images[xx],(v[x][0],v[x][1]),2,(0,0,255),3)
    			tmpIm = images[xx]
    			images[xx] = cv2.cvtColor(images[xx], cv2.COLOR_BGR2GRAY)
    			cv2.circle(mask,(v[x][0],v[x][1]),v[x][2],(0,0,0),-1)
    			cv2.bitwise_or(images[xx],mask,mask)
    			ZerosCount = (mask.shape[0]*mask.shape[1]) - np.count_nonzero(mask)
    			Question.append(ZerosCount)
                # cv2.namedWindow("White",cv2.WINDOW_AUTOSIZE)
    			# cv2.moveWindow("White", 0, 0)
    			#cv2.imshow("White",mask)
    			# cv2.waitKey(0)
    			# cv2.destroyAllWindows()
    			mask =255 *  np.ones((images[xx].shape),np.uint8)
    			pass
    		index, value = max(enumerate(Question), key=operator.itemgetter(1))
    		for ds in xrange(0,len(Question)):
    			if ds == index:
    				continue
    				pass
    			if abs(value-Question[ds]) < 61 and value > 207:
    				doubled = True
    			pass
    		if ModelaAnswer[k+offset2] == index and not doubled and value > 207:
    			correct+=1
    		if show == 1:
    		    print Question , index+1#offset+=15    
        # for i in circles:
           #  #draw the outer circle
           # cv2.circle(images[xx],(i[0],i[1]),i[2],(0,255,0),2)
           #  #draw the center of the circle
           # cv2.circle(images[xx],(i[0],i[1]),2,(0,0,255),3)
           # pass
        if show == 1:
            print correct
        offset2+=15
        if show == 1:
        	cv2.namedWindow(direct,cv2.WINDOW_AUTOSIZE)
        	cv2.moveWindow(direct, 0, 0)
        	#cv2.resizeWindow(direct, 700,700)
        	cv2.imshow(direct,tmpIm)
        	cv2.waitKey(0)
        	cv2.destroyAllWindows()
        	pass
        # for k,v in FinalCircles.items():
        #     print k , v
        #     pass
    print name , correct
    f.write(name + "," + str(correct) + "\n")
    del correct
    del flag
    del images
    del image
    del Xaxis
    del mask
    del whitePage
    del offset2
    del offset
    del k
    del FinalCircles
    del SortedCircles
    del circles

