import cv2
import pickle
import cvzone
import numpy as np



capture = cv2.VideoCapture('ParkingVid.mp4')

with open('carParkingPos', 'rb') as f:
    positionsList = pickle.load(f)

width, height = 107, 48

def checkParkingSpaces(afterImage):
    ParkingSpaceCounter = 0

    for pos in positionsList:
        x,y = pos

        imageCrop = afterImage[y:y+height,x:x+width]
        #cv2.imshow(str(x*y),imageCrop)
        count = cv2.countNonZero(imageCrop)
        cvzone.putTextRect(img,str(count),(x,y+height-3),scale=1,thickness=2,offset=0)

        if count < 850:
            color = (0,255,0)
            thickness = 5
            ParkingSpaceCounter += 1
        else:
            color = (0,0,255)
            thickness = 2
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height),color, thickness)

    cvzone.putTextRect(img, str(ParkingSpaceCounter), (100,50), scale=3, thickness=3, offset=20, colorR = (0,200,0))


while True:

    if capture.get(cv2.CAP_PROP_POS_FRAMES) == capture.get(cv2.CAP_PROP_FRAME_COUNT):
        capture.set(cv2.CAP_PROP_POS_FRAMES,0)

    success, img = capture.read()
    imageGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imageBlur = cv2.GaussianBlur(imageGray,(3,3),1)
    imageThreshold = cv2.adaptiveThreshold(imageBlur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,16)

    imageMedian = cv2.medianBlur(imageThreshold,5)
    kernel = np.ones((3,3),np.uint8)
    imageDilate = cv2.dilate(imageMedian,kernel, iterations = 1)  # to make pixels big

    checkParkingSpaces(imageDilate)


    cv2.imshow("Image",img)
    #cv2.imshow("ImageBlur", imageThreshold)
    cv2.imshow("ImageMedian",imageMedian)  # median is used to reduce noise
    cv2.waitKey(10)