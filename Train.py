import cv2 as cv
import numpy as np 
import os          # NumPy is a Python library used for working with arrays.
from os import listdir 
from PIL import Image 

    # The OS module in Python provides functions for interacting with the operating system
    # This module provides a portable way of using operating system-dependent functionality.
from os.path import isfile,join 
    # This module contains some useful functions on pathnames. The path parameters are either strings or bytes . These functions here are used for different purposes such as for merging, normalizing and retrieving path names in python . 
 


def trainclassifier ():
    data_path ='facephoto/'
    path = [join(data_path ,file) for file in listdir(data_path)]
      
    faces = []
    ids = []

    for image in path:
        img =Image.open(image).convert('L')
        imagenp =np.array(img , 'uint8')
        id= int(os.path.split(image)[1].split('.')[1])
      
        faces.append(imagenp)
        ids.append(id)
        cv.imshow("Training data" , imagenp)
        cv.waitKey(1)==13

    ids = np.array(ids)

    Model = cv.face.LBPHFaceRecognizer_create()

    Model.train(faces ,ids)

    Model.write('lbph_classifier.yml')
    print("done.......................................................")
    cv.destroyAllWindows()



