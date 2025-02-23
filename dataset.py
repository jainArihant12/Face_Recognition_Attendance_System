import cv2       
import numpy as np

face_classifier = cv2.CascadeClassifier('har_face.xml')

#to extract property of an image
# img is capture in rgb but we will convert into Gray scale

def face_extractor(img):

    gray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY) 
    face = face_classifier.detectMultiScale(gray , 1.3,5)

    if face is ( ):
        return None
    #Cropping of face
    for (x,y,w,h) in face:
        crop_face = img[y:y+h , x:x+w]

    return  crop_face


    

    