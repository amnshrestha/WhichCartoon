import cv2
import numpy as np
import os

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

webCam = cv2.VideoCapture(0)
possibleImage = cv2.imread("./cartoonImages/Spongebob.png")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR,"cartoonImages")

imagesFound = []

for root, dirs, files in os.walk(image_dir):
    for file in files:
        if file.endswith("png") or file.endswith("jpeg"):
            filePath = "./cartoonImages/"+file
            imageToPut = cv2.imread(filePath)
            imagesFound.append(imageToPut)

while True:

    # Capture the image from each frame 
    ret, img = webCam.read()
    grayScale = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(grayScale, scaleFactor=1.5, minNeighbors=5)
    for (x,y,w,h) in faces:
        color = (255,0,0)
        stroke = 2

        # Rectangle that shows the face
        cv2.rectangle(img, (x, y), (x+w, y+h), color, stroke)

        # Coordinates for the box above
        newColor = (0,255,0)
        newStroke = 4

        xStartingPosition = int(((x + x + w)/2) - (possibleImage.shape[1] / 2))

        # shape[1] is width and shape[0] is height
        yStart = 0
        if(y-possibleImage.shape[0]> 0):
            yStart = y-possibleImage.shape[0]

        img[yStart:yStart+possibleImage.shape[0], xStartingPosition:xStartingPosition+possibleImage.shape[1]] = possibleImage

        # cv2.rectangle(img, (x, y-300),(x+w, y),newColor, newStroke)
        
        

    # Display the resulting frame 
    cv2.imshow('frame',img)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

webCam.release()
cv2.destroyAllWindows()
