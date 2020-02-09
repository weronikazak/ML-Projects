# Hough Line Tranformation
import cv2
import numpy as np

img = cv2.imread('images/sudoku.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 200, 100, apertureSize=3)
img2 = img.copy()

# ------------------------
# STANDARD HOUGH TRANSFORM
# ------------------------


lines = cv2.HoughLines(edges, 1, np.pi/180, 200)
#threshld - minimum value for it to be considered as a line
for line in lines:
    for rho, theta in line:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))

        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 2)

cv2.imwrite('images/houghlines.jpg',img)

# -----------------------------
# PROBABILISTIC HOUGH TRANSFORM
# -----------------------------
# cv2.HoughLinesP((...), minLineLength, maxLineGap)
# minLineLength - Minimum length of line. Line segments shorter than this are rejected.
# maxLineGap - Maximum allowed gap between line segments to treat them as single line.

minLineLength = 100
maxLineGap = 10
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength, maxLineGap)
for line in lines:
    for x1, y1, x2, y2 in line:
        cv2.line(img2, (x1, y1), (x2, y2), (0, 255, 0), 2)

cv2.imwrite('images/houghlinesP.jpg', img2)