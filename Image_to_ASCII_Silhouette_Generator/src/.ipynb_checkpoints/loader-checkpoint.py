import cv2
import numpy as np
import PIL

img = cv2.imread("example/dog.jpg")
(h, w, c) = img.shape()
print("hight : ", h)
print("width : " ,w)
print("c : ", c) 
# cv2.imshow('image', img)

