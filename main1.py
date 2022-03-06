import cv2
import pickle
import cvzone
import numpy as np

# video feed
cap = cv2.VideoCapture('Carparkvid.mp4')

width, height = 20, 8

with open('CarParkPos', 'rb') as f:
    poslist = pickle.load(f)

print(poslist)
def checkparkingspace(imgPro):
    for pos in poslist:
        x, y = pos
        imgCrop = imgPro[y:y+height,x:x+width]
        #cv2.imshow(str(x*y),imgCrop)
        count=cv2.countNonZero(imgCrop)
        cvzone.putTextRect(img, str(count), (x,x+height-5))
while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, img = cap.read()
    imgGray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur=cv2.GaussianBlur(imgGray,(3,3),1)
    imgThreshold=cv2.adaptiveThreshold(imgBlur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,16)
    imgMedian= cv2.medianBlur(imgThreshold, 5)
    kernel=np.ones((3,3),np.uint8)
    imgdialates=cv2.dilate(imgMedian, kernel, iterations=1)
    checkparkingspace(imgdialates)
    for pos in poslist:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 1)
    cv2.imshow("Image", img)
    #cv2.imshow("Imageblur",imgBlur)
    #cv2.imshow("ImageThresh",imgThreshold)
    #cv2.imshow("ImageMedian",imgMedian)
    #cv2.imshow("Imagedilates",imgdialates)
    cv2.waitKey(1)
