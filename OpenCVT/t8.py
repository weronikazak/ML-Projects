# performance measurement
import cv2
import numpy as np

# ----------------
#    MEASURING
# ----------------

cv2.setUseOptimized(True)
# optimized:      0.6774659
# non-optimized:  0.9942197

e1 = cv2.getTickCount()

img = cv2.imread('img.jpg')
for i in range(5, 49, 2):
    img = cv2.medianBlur(img, i)

e2 = cv2.getTickCount()
t = (e2 - e1)/cv2.getTickFrequency()

print(t)
