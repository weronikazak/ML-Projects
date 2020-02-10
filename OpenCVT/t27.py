# HARRIS CORNER DETECTION
import cv2
import numpy as np

img = cv2.imread('images/cubes.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
gray = np.float32(gray)

dst = cv2.cornerHarris(gray, 2, 3, 0.04)
# cv2.cornerHarris(img, blockSize, ksize, k)
# img - input grayscale and float32 image
# blocksie - size of neighbourhood for corner detection
# ksize - parametr pochodnej Sobela
# k - Harris detector free parameter w równaniu

# wynik jest rozszerzony w celu zaznaczenia narożników
dst = cv2.dilate(dst, None)

# threshld for an optimal value
img[dst>0.01*dst.max()] = [0, 0, 255]

cv2.imshow('dst', img)
if cv2.waitKey(0) & 0xFF == ord('q'):
    cv2.destroyAllWindows()


# -----------------
# SUBPIXEL ACCURACY
# -----------------
ret, dst = cv2.threshold(dst, 0.01*dst.max(), 255, 0)
dst = np.uint8(dst)

# find centroids
ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)

# defining criteria to stop and refine the corners
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
corners = cv2.cornerSubPix(gray, np.float32(centroids), (5, 5), (-1, -1), criteria)

res = np.hstack((centroids, corners))
res = np.int0(res)
img[res[:, 1], res[:,0]] = [0, 0, 255]
img[res[:, 3], res[:, 2]] = [0, 255, 0]

cv2.imwrite('images/subpixel.jpg', img)