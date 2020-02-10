# FAST
import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('images/line.jpg', 0)
fast = cv2.FastFeatureDetector_create()

kp = fast.detect(img, None)

img2 = cv2.drawKeypoints(img, kp, None, color=(255, 0, 0))


print("Threshold: ", fast.getThreshold())
print("nonmxSuppression: ", fast.getNonmaxSuppression())
print ("neighborhood: ", fast.getType())
print("Total Keypoints with nonmaxSuppression: ", len(kp))

cv2.imwrite('images/fast_true.png', img2)

# fast.setNonmaxSuppression = False
# kp = fast.detect(img, None)

# print("Total Keypoints without nonmaxSupression: ", len(kp))

# img3 = cv2.drawKeypoints(img, kp, color=(0, 255, 255))

# cv2.imwrite('images/fast_false.png')