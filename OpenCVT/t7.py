# bitwise, bluring
# Icon made by https://www.flaticon.com/authors/ddara
import cv2
import numpy as np

x = np.uint8([250])
y = np.uint8([10])

# -----------------
#  IMAGE ADDITION
# -----------------


# CV2 img addition
print(cv2.add(x, y)) # 250 + 10 = 260 => 255
# NumPy img addition
print(x + y)         # 250 + 10 = 26- % 256 = 4


# -----------------
#    IMAGE BLUR
# -----------------

# img1 = cv2.imread('img.jpg')
# img2 = cv2.imread('img1.jpg')

# dst = cv2.addWeighted(img1, 0.7, img2, 0.3, 0)

# cv2.imshow('dst', dst)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# ------------------
# BITWISE OPERATION
# ------------------

img1 = cv2.imread('img.jpg')
img2 = cv2.imread('plant.png')

# putting logo on top-left corner
rows, cols, channels = img2.shape
# create a ROI
roi = img1[0:rows, 0:cols]

# create a mask of logo and create its inverse mask
img2gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
mask_inv = cv2.bitwise_not(mask)

# black-out the are of logo in ROI
img1_bg = cv2.bitwise_and(roi, roi, mask = mask_inv)

# take only region of logo from logo image
img2_fb = cv2.bitwise_and(img2, img2, mask = mask)

# put logo in ROI and modify the main image
dst = cv2.add(img1_bg, img2_fb)
img1[0:rows, 0:cols] = dst

cv2.imshow('res', img1)
cv2.waitKey(0)
cv2.destroyAllWindows()