# thresholding
import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('images/cat.jpg', 0)

ret, thresh1 = cv2.threshold(img, 126, 255, cv2.THRESH_BINARY)
ret, thresh2 = cv2.threshold(img, 126, 255, cv2.THRESH_BINARY_INV)
ret, thresh3 = cv2.threshold(img, 126, 255, cv2.THRESH_TRUNC)
ret, thresh4 = cv2.threshold(img, 126, 255, cv2.THRESH_TOZERO)
ret, thresh5 = cv2.threshold(img, 126, 255, cv2.THRESH_TOZERO_INV)

titles = ['Original', 'Binary', 'Binary_Zero', 'Trunc',
                    'Zero', 'Zero_Inv']
images = [img, thresh1, thresh2, thresh3, thresh4, thresh5]


for i in range(6):
    plt.subplot(2,3, i+1)
    plt.imshow(images[i], 'gray')
    plt.title(titles[i])
    plt.xticks([])
    plt.yticks([])

plt.show()


# -----------------------
#   ADAPTIVE THRESHOLDING
# -----------------------

img1 = cv2.imread('images/photo.jpg', 0)
img1 = cv2.medianBlur(img1, 5)

ret, th1 = cv2.threshold(img1, 127, 255, cv2.THRESH_BINARY)

th2 = cv2.adaptiveThreshold(img1, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
th3 = cv2.adaptiveThreshold(img1, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY, 11, 2) 

titles1 = ['Original', 'Binary', 'Adaptive_Mean', 'Adaptive_Gaussian']
images1 = [img1, th1, th2, th3]

for i in range(4):
    plt.subplot(2, 2, i+1)
    plt.imshow(images1[i], 'gray')
    plt.title(titles1[i])
    plt.xticks([])
    plt.yticks([])
plt.show()