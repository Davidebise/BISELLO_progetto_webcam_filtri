import cv2
import numpy as np

def gray(frame):
    gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return cv2.cvtColor(gray_img, cv2.COLOR_GRAY2BGR)

def negative(frame):
    return cv2.bitwise_not(frame)

def sepia(frame):  
    img_sepia = cv2.transform(frame, np.matrix([[0.272, 0.534, 0.131],
                                                [0.349, 0.686, 0.168],
                                                [0.393, 0.769, 0.189]]))
    return cv2.convertScaleAbs(img_sepia)