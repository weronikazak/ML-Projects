# image smoothing
import cv2
import numpy as np
from matplotlib import pylab as plt

img = cv2.imread('images/img.jpg')

# -----------------
#  2D CONVOLUTION
# -----------------

# aka Image Filtering
# multypling each pixel in a matrice by 1/25
# result: blurred image

kernel = np.ones((5, 5), np.float32)/25
dst = cv2.filter2D(img, -1, kernel)

plt.subplot(121)
plt.imshow(img)
plt.title('Original')
plt.xticks([])
plt.yticks([])

plt.subplot(122)
plt.imshow(img)
plt.title('Averaging')
plt.xticks([])
plt.yticks([])

# ---------------
# IMAGE BLURRING
# ---------------

# Averaging

blur = cv2.blur(img, (5, 5))

plt.subplot(123)
plt.imshow(blur)
plt.title('Blurred')
plt.xticks([])
plt.yticks([])

# Gaussian Blurring
# width and height of kernel and standard deviation
# only similiar initensity to center pixels
# doesn't care about edges

g_blur = cv2.GaussianBlur(img, (5,5), 0)

plt.subplot(124)
plt.imshow(g_blur)
plt.title('Gaussian')
plt.xticks([])
plt.yticks([])

# Median Blur
# each pixel is replaced with its median value. kernel value should be odd
# hightly effective in salt-and-pepper noise in images

median = cv2.medianBlur(img, 5) # 50% noise

plt.subplot(125)
plt.imshow(median)
plt.title('Median')
plt.xticks([])
plt.yticks([])

# Bilateral Filtering
# only nearby pixels are considered for blurring
# slightly effective when keeping edges sharp

bil = cv2.bilateralFilter(img, 9, 75, 75)

plt.subplot(126)
plt.imshow(bil)
plt.title('Bilateral')
plt.xticks([])
plt.yticks([])
plt.show()