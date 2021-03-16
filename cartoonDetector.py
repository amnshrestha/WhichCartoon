import cv2
import numpy as np
import os
from random import seed
from random import randint

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') #Loading the model
webCam = cv2.VideoCapture(0) #Initializing the camera

#Getting all the image files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR,"cartoonImages")

imagesFound = []#List to store the images

for root, dirs, files in os.walk(image_dir):
    for file in files:
        if file.endswith("png") or file.endswith("jpeg"):
            filePath = "./cartoonImages/"+file
            imageToPut = cv2.imread(filePath)
            imagesFound.append(imageToPut)

FrameSkip = 1 #Kept here in case we want to change the speed later
currentFrame = 0
endFrame = 40 #Increase this for suspense

possibleImage = imagesFound[0]


while True:

    


    # Capture the image from each frame 
    ret, img = webCam.read()
    grayScale = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(grayScale, scaleFactor=1.5, minNeighbors=5)
    for (x,y,w,h) in faces:

        if(currentFrame < endFrame):
            if(currentFrame % FrameSkip == 0):
                index = randint(0,len(imagesFound) - 1)
                possibleImage = imagesFound[index]
            currentFrame+=1

        color = (255,0,0)
        stroke = 2
        # Rectangle that shows the face
        cv2.rectangle(img, (x, y), (x+w, y+h), color, stroke)

        # shape[1] is width and shape[0] is height
        xStartingPosition = int(((x + x + w)/2) - (possibleImage.shape[1] / 2))
        yStart = 0
        if(y-possibleImage.shape[0]> 0):
            yStart = y-possibleImage.shape[0]

        img[yStart:yStart+possibleImage.shape[0], xStartingPosition:xStartingPosition+possibleImage.shape[1]] = possibleImage

        # Coordinates for the box with cartoon
        if(currentFrame >= endFrame):
            newColor = (0,255,0)
            newStroke = 2
            xEnd = xStartingPosition + possibleImage.shape[1]
            yEnd = yStart + possibleImage.shape[0]
            cv2.rectangle(img, (xStartingPosition, yStart), (xEnd, yEnd), newColor, newStroke)
            # cv2.rectangle(img, (xStartingPosition, yStart),(xStartingPosition + possibleImage[1], yStart + possibleImage[0]),newColor, newStroke)
       
        

    # Display the resulting frame 
    cv2.imshow('frame',img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        print("Exiting")
        break
    if cv2.waitKey(10) & 0xFF == ord('r'):
        print("Restarting")
        currentFrame = 0

webCam.release()
cv2.destroyAllWindows()
