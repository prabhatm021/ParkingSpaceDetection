import cv2
import pickle

img = cv2.imread('ParkingImg.png')

width, height = 107, 48

try:
    with open('carParkingPos', 'rb') as f:
        positionsList = pickle.load(f)
except:
    positionsList =[]

def mouseClick(events,x,y,flags,params):
    if events == cv2.EVENT_LBUTTONDOWN:
        positionsList.append((x,y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(positionsList):
            x1,y1 = pos
            if x1 < x < x1+width and y1 < y < y1 + height:
                positionsList.pop(i)

    with open('carParkingPos', 'wb') as f:
        pickle.dump(positionsList,f)

while True:
    #cv2.rectangle(img,(50,192),(157,240),(255,0,255),2)
    img = cv2.imread('ParkingImg.png')
    for pos in positionsList:
        cv2.rectangle(img, pos, (pos[0]+width, pos[1]+height), (255, 0, 255), 2)

    cv2.imshow("Image",img)
    cv2.setMouseCallback("Image", mouseClick)
    cv2.waitKey(1)