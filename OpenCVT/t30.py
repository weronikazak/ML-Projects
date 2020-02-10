# SURF
import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('images/sudoku.jpg', 0)
surf = cv2.xfeatures2d.SURF_create()

kp, des = surf.detectAndCompute(img, None)

print(len(kp))

print(surf.hessianThreshold)

surf.hessianThreshold = 5000

kp, des = surf.detectAndCompute(img, None)

print(len(kp))

img2 = cv2.drawKeypoints(img, kp, None, (255, 0, 0), 4)

plt.imshow(img2)
plt.show()

print(surf.descriptorSize())

surf.extended = True
kp, des = surf.detectAndCompute(img, None)
print(surf.descriptorSize())

print(des.shape)


