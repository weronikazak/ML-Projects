# translating, scaling, tranformations
import cv2
import numpy as np

img = cv2.imread('images/img.jpg')

# ------------
#   SCALING
# ------------


res = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

# OR

height, width = img.shape[:2]
res = cv2.resize(img, (2*width, 2*height), interpolation=cv2.INTER_CUBIC)


# -------------
#  TRANSLATION
# -------------


rows, cols, ch = img.shape
# M as matrice
M = np.float32([[1, 0, 100], [0, 1, 50]])
dst = cv2.warpAffine(img, M, (cols, rows))
# cv2.warpAffine() - size of the output image, should be in form of (width, height)
# takes 2x3 transformation matrix as input

cv2.imshow('img', dst)
cv2.waitKey(0)
cv2.destroyAllWindows()


# -------------
#   ROTATION
# -------------


M = cv2.getRotationMatrix2D((cols/2, rows/2), 90, 1)
dst = cv2.warpAffine(img, M, (cols, rows))


# --------------------
# AFFINE TRANFORMATION
# --------------------


from matplotlib import pyplot as plt

rows, cols, ch = img.shape

pts1 = np.float32([[50, 50], [200, 50], [50, 200]])
pts2 = np.float32([[10, 100], [200, 50], [100, 250]])

M = cv2.getAffineTransform(pts1, pts2)

dst = cv2.warpAffine(img, M, (cols, rows))

plt.subplot(121)
plt.imshow(img)
plt.title('Input')

plt.subplot(121)
plt.imshow(dst)
plt.title('Output')

plt.show()


# --------------------------
# PERSPECTIVE TRANSFORMATION
# --------------------------

img = cv2.imread('images/photo.jpg')
rows, cols, ch = img.shape

pts1 = np.float32([[50, 50], [123, 45], [10, 40], [158, 90]]) # points on original image,
# non-transformated, f.e.: corners of a drawn on a paper box
pts2 = np.float([0, 0], [300, 0], [0, 300], [300, 300])
# shape of transhormed image

M = cv2.getPerspectiveTransform(pts1, pts2)

dst = cv2.warpPerspective(img, M, (300, 300))

plt.subplot(121)
plt.imshow(img)
plt.title('Input')

plt.subplot(122)
plt.imshow(dst)
plt.title('Output')