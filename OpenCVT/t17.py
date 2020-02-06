# CONTOURS
import cv2
import numpy as np

img = cv2.imread("images/img.jpg", 0)
ret, thresh = cv2.threshold(img, 127, 255, 0)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# 1 - source img, 2 - contour retrieval mode, 3 - contour approximation method
# outputs contours and hierarchy
# each individual contour is a numy array of (x, y) coordinates of boundary points of object

# draws all the contours
cv2.drawContours(img, contours, -1, (0, 255, 0), 3)

# draws an individual contours, here its the fourth one
cv2.drawContours(img, contours, 3, (0, 255, 0), 3)
# or
cnt = contours[4]
cv2.drawContours(img, [cnt], (0, 255, 0), 3)

while True:
    cv2.imshow('img', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

# CHAIN_APPROX_NONE - all the boundary points are stored (f. e. całe obramowanie)
# CHAIN_APPROX_SIMPLE - only 4 points are stored (tylko kąty)