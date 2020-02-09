# HOUGH CIRCLE TRANSFORMATION
import cv2
import numpy as np

img = cv2.imread('images/orange.jpg', 0)
img = cv2.medianBlur(img, 5)
cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 20,
                param1=60, param2=30, minRadius=10, maxRadius=120)
# param1 - higher threshold passed to Canny edge detector
# param2 - accumulator threshold for the circle centers at the detection stage.
# The smaller it is, the more false circles may be detected.

circles = np.uint16(np.around(circles))
for i in circles[0, :]:
    # outer circle
    cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 2)
    # center of the image
    cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 3)

cv2.imshow('circles', cimg)
cv2.waitKey(0)
cv2.destroyAllWindows()