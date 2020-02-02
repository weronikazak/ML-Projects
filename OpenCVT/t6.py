# basic

import cv2
import numpy as np

# ----------------
#      PIXELS
# ----------------
img = cv2.imread('img.jpg')
# select pixel by position (row, column)
# returning as its BGR values
px = img[100, 100]

# access only Blue/Green/Red (0, 1, 2) value
px = img[100, 100, 1] # returns Green value

# modifying pixels
img[100, 100] = [255, 255, 255]

# better pixels modifying
# accessing Red value
img.item(10, 10, 2)

# modyfing Red value
img. itemset((10, 10, 2), 100)
img.item(10, 10, 2) # will return 100

# ----------------
# IMAGE PROPERTIES
# ----------------

print(img.shape) #  returns a tuple of nr of rows, columns and chanel
print(img.size)  # gives total number of pixels
print(img.dtype) # gives datatype. here it's uint8

# ----------------
#       ROI
# ----------------

# copying and pasting an eye
eye = img[185:220, 225:295]
img[120:155,145:215] = eye


# ------------------
#      CHANNELS
# ------------------

b, g, r =cv2.split(img)
img = cv2.merge((b, g, r))
# b = img[:, :, 0]
img[:, :, 2] = 0 # all red pixels to 0


# ------------------
#     BORDERS
# ------------------

from matplotlib import pyplot as plt

BLUE = [255, 0, 0]

img1 = cv2.imread('imgC.jpg')

replicate = cv2.copyMakeBorder(img1, 10, 10, 10, 10, cv2.BORDER_REPLICATE)
reflect = cv2.copyMakeBorder(img1, 10, 10, 10, 10, cv2.BORDER_REFLECT)
reflect101 = cv2.copyMakeBorder(img1, 10, 10, 10, 10, cv2.BORDER_REFLECT_101)
wrap = cv2.copyMakeBorder(img1, 10, 10, 10, 10, cv2.BORDER_WRAP)
constant = cv2.copyMakeBorder(img1, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=BLUE)


plt.subplot(231),plt.imshow(img1, 'gray'), plt.title('ORIGINAL')
plt.subplot(232),plt.imshow(replicate, 'gray'), plt.title('REPLICATE')
plt.subplot(233),plt.imshow(reflect, 'gray'), plt.title('REFLECT')
plt.subplot(234),plt.imshow(reflect101, 'gray'), plt.title('REFLECT101')
plt.subplot(235),plt.imshow(wrap, 'gray'), plt.title('WRAP')
plt.subplot(236),plt.imshow(constant, 'gray'), plt.title('CONSTANT')

plt.show()


while True:
    cv2.imshow('img', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
