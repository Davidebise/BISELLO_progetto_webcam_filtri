import cv2
import numpy as np

def gray(frame):
    output = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return output