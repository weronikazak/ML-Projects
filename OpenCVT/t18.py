# Contours features
import cv2
import numpy as np

img = cv2.imread('star.jpg', 0)
ret, thresh = cv2.threshold(img, 127, 255, 0)
contours, hierarchy = cv2.findContours(thresh, 1, 2)

# ----------
#  MOMENTS
# ----------

cnt = contours[0]
M = cv2.moments(cnt)
print(M)

# ------------
# CONTOUR AREA
# ------------

area = cv2.contourArea(cnt)
#or
area = M['m00']
print(area)

# ----------------------
# CONTROUR APPROXIMATION
# ----------------------
# przybliża kaształt konturu do innego kształtu
# epsilon to max odległość od konturu do przybliżonego konturu (aka parmetr dokładności)

epsilon = .1 * cv2.arcLength(cnt, True)
approx = cv2.approxPolyDP(cnt, epsilon, True)

# ------------
# CONVEX HULL
# ------------
# np. 'obramowanie' ręki
# hull = cv2.convexHull(points[, hull[, clockwise[, returnPoints]]])
# points     - contrours passed into
# hull       - output (usually avoided)
# clockwise  - orientation flag ( if True => returns the coordionates of hull points,
# if False => returns indices of contour points corresponding to the hull points)

hull = cv2.convexHull(cnt)

# ------------------
# CHECKING CONVEXITY
# ------------------
# convexity - wypukłość / wygięcie
# funkcja zwraca True lub False w zależności od tego czy curve jest wypukłe

k = cv2.isContourConvex(cnt)

# ------------------
# BOUNDING RECTANGLE
# ------------------

# Straight Bounding Rectangle
# nie uwzględnia przekrzywienia obiektu

x, y, w, h = cv2.boundingRect(cnt)
cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Rotated Rectangle

rect = cv2.minAreaRect(cnt) # zwraca Box2D w postaci:
# ( center, (x, y), (width, height), angle_of_rotation)
box = cv2.boxPoints(rect)
box = np.int0(box)
cv2.drawContours(img, [box], 0, (0, 0, 255), 2)

# ---------------------
# MIN. ENCLOSING CIRCLE
# ---------------------
# podobne do Rectangle Boundary, tylko, że obiekt jest w kole

(x, y), radius = cv2.minEnclosingCircle(cnt)
center = (int(x), int(y))
radius = int(radius)
cv2.circle(img, center, radius, (255, 0, 0), 2)

# -----------
#   ELIPSE
# -----------

ellipse = cv2.fitEllipse(cnt)
cv2.ellipse(img, ellipse, (0, 255, 0), 2)

# -------
#  LINE
# -------

rows, cols = img.shape[:2]
[vx, vy, x, y] = cv2.fitLine(cnt, cv2.DIST_L2, 0, 0.01, 0.01)
lefty = int((-x*vy/vx) + y)
righty = int(((cols - x) * vy/vx) + y)
cv2.line(img, (cols - 1, righty), (0, lefty), (0, 255, 0), 2)