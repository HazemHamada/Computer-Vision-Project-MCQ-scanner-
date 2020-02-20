import numpy as np
import cv2
import math
import imutils

def correctRotation(img):
    img_before = img#copy the image
    _,img_gray = cv2.threshold(img_before,127,255,cv2.THRESH_BINARY)#Threshold the image colores
    img_edges = cv2.Canny(img_gray, 100, 100, apertureSize=3)#recognize the edges in the image
    lines = cv2.HoughLinesP(img_edges, 1, math.pi / 180.0, 100, minLineLength=100, maxLineGap=5)#get the lines and there angles
    #extract the angeles in one array
    angles = []
    for x1, y1, x2, y2 in lines[0]:
        cv2.line(img_before, (x1, y1), (x2, y2), (255, 0, 0), 3)
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
        angles.append(angle)
    median_angle = np.median(angles)#compute the median angle
    img_rotated=imutils.rotate(img_before, median_angle)#rotate the image with the computed median angle
    return img_rotated

def getAllCircles(img,min,max):
    res=img#copy the image
    circles=cv2.HoughCircles(res,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=min,maxRadius=max)#recognize the circles in the by hough transform
    if not(circles is None):#check if the circles array if empty or not
        circles=np.uint16( np.around(circles))#convert the array into integers
        #mark the circles
        for i in circles[0,:]:
           cv2.circle(res,(i[0],i[1]),i[2],(170,200,170),2)
           cv2.circle(res, (i[0], i[1]), 2,(170, 200, 170), 3)
    else:
        print("WARNING: the image contains no circles!!!")
    return res,circles

def getFilledCircles(img,min,max):
    res = img#copy the image
    _, res = cv2.threshold(res, 130, 255, cv2.THRESH_BINARY)#threshold the image to extract the filled circles only
    circles = cv2.HoughCircles(res, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=13, minRadius=min, maxRadius=max)#recognize the circles by hough transform
    if not (circles is None):#check if the circles array if empty or not
        circles = np.uint16(np.around(circles))#convert the array into integers
        #mark the cricles
        for i in circles[0, :]:
            cv2.circle(res, (i[0], i[1]), i[2], (170, 200, 170), 2)
            cv2.circle(res, (i[0], i[1]), 2, (170, 200, 170), 3)
    else:
        print("WARNING: the image contains no circles!!!")
    return res,circles

def arrangeCircles(circles):
    #it is like the normal bubble sort but with different compareson function 
    res = circles
    #arrange with respect to Y-axis
    swapped = True
    while swapped:
        swapped = False
        for i in range(int(np.size(res[:, :, [1]] / 2) - 1)):
            if res[:, i, [1]] > res[:, i + 1, [1]]:
                res[:, i, [0, 1]], res[:, i + 1, [0, 1]] = res[:, i + 1, [0, 1]], res[:, i, [0, 1]]
                swapped = True
    #arrange with respest to X-axis
    swapped = True
    while swapped:
        swapped = False
        for i in range(int(np.size(res[:,:,[0]]/2)-1)):
            if res[:,i,[0]] > res[:,i+1,[0]] and rangeEqual(res[:, i, [1]], res[:, i+1, [1]]):
                res[:,i,[0,1]], res[:,i + 1,[0,1]] = res[:,i + 1,[0,1]], res[:,i,[0,1]]
                swapped = True
    return res

def rangeEqual(j,k):
    #compare with a range +3 and -3 
    for i in range(-3,4):
        if (j+i)==k or (k+i)==j:
            return True
    return False

def scann(all_Circles, filled_Circles):
    allCircles=all_Circles[:,:,[0,1]]
    filledCircles=filled_Circles[:,:,[0,1]]
    co=0
    flag=np.zeros(int(np.size(allCircles[:, :, [0, 1]])/2))#the flag masking the the positions of the filled circles in all the circles
    for i in range(int(np.size(allCircles[:, :, [0, 1]]) / 2)):#flaging the mask
        for j in range(int(np.size(filledCircles[:, :, [0, 1]]) / 2)):
            if rangeEqual(allCircles[:, i, [1]], filledCircles[:, j, [1]]) and rangeEqual(filledCircles[:, j, [0]], allCircles[:, i, [0]]):
                flag[i] = 1

    genderArr=np.array(["Male","Female"])
    semesterArr=np.array(["Fall","Spring","Summer"])
    programArr=np.array(["MCTA","ENVER","BLDG","CESS","ERGY","COMM","MANF","LAAR","MATL","CISE","HAUD"])
    answersArr=np.array(["Strongly Agree","Agree","Neutral","Disagree","Strongly Disagree"])
    gender=""
    semester=""
    program=""
    answers=[]
    #generate the output
    for i in range(2):
        if flag[i]==1:
            gender=genderArr[i]

    for i in range(3):
        if flag[i+2]==1:
            semester=semesterArr[i]

    for i in range(11):
        if flag[i+5]==1:
            program=programArr[i]

    for j in range(19):
        for i in range(5):
            if flag[19+i+j*5]==1:
                answers.append(answersArr[i])
                continue

    return gender, semester, program, answers
