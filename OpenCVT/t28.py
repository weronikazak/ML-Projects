# SHI-THOMAS CORNER DETECTOR
import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('images/cubes.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

corners = cv2.goodFeaturesToTrack(gray, 50, 0.02, 10)
# finds N strongest corners in the image by Shi-Tomas methode
# cv2.goodFeaturesToTrack(img, maxCorners, qualityLevel, minDistance)
# img - grayscale image
# maxCorners - number of corners you want to find
# qualityLevel - specify quality level (0, 1), denotes the minimum 
# quality of corner, the others below are rejected
# minDistance - minimmum euclidean distance between detected corners

corners = np.int0(corners)

for i in corners:
    x, y = i.ravel()
    cv2.circle(img, (x, y), 3, 255, -1)

plt.imshow(img)
plt.show()
