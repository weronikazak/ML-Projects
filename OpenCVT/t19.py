# WŁASNOŚCI KONTURÓW
import cv2
import numpy as np

img = cv2.imread('star.jpg', 0)
ret, thresh = cv2.threshold(img, 127, 255, 0)
contours, hierarchy = cv2.findContours(thresh, 1, 2)

cnt = contours[0]

# ------------
# ASPECT RADIO
# ------------
# stosunek szerokości do wysokości boundary prostokata

x, y, w, h = cv2.boundingRect(cnt)
aspect_ratio = float(w)/h

# -----------
#   EXTENT
# -----------
# stosunek powerzchni konturu do bounding rectangle area

area = cv2.contourArea(cnt)
x, y, w, h = cv2.boundingRect(cnt)
rect_area = w*h
extent = float(area)/rect_area

# ---------
#  SOLTIDY
# ---------
# solidność to stosunek powierzchni konturu do jego convex hullu

hull = cv2.convexHull(cnt)
hull_area = cv2.contourArea(hull)
soltidy = float(area)/hull_area

# -------------------
# EQUIVALENT DIAMETER
# -------------------
# średnica równoważna - średnica koła, którego pole powierzchni jest
# takie jak pole konturu

equi_diameter = np.sqrt(4*area/np.pi)

# --------------
#  ORIENTATION
# --------------
# kąt, pod którym obiekt jest skierowany
# poniższa funkcja podaje również Major Axis (długość osi głownej)
# oraz Minor Axis (długość osi mniejszej)

(x, y), (MA, ma), angle = cv2.fitEllipse(cnt)


# ---------------------
# MASK AND PIXEL POINTS
# ---------------------
# w niektórych przypadkach potrzebne są wszystkie punkty, które składają
# się na jakiś obiekt. można je uzyskać za pomocą numpy i funkcji cv2
# różnica jest znikoma. output numpy to (x, y), cv2 z kolei to (row, col)
# jednak x = row, y = col

mask = np.zeros(img.shape, np.uint8)
cv2.drawContours(mask, [cnt], 0, 255, -1)
pixelpoints = np.transpose(np.nonzero(mask))
# pixelpoints = cv2.findNonZero(mask)

# -------------------------------------
# MAX. & MIN. VALUE AND THEIR LOCATIONS
# -------------------------------------

min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(img, mask-mask)

# ----------------------------
# MEAN COLOUR / MEAN INTENSITY
# ----------------------------
# średni kolor lub natężenie dla obiektu

mean_val = cv2.mean(img, mask=mask)

# ---------------
# EXTREME POINTS
# ---------------

leftmost = tuple(cnt[cnt[:, :, 0].argmin()][0])
rightmost = tuple(cnt[cnt[:, :, 0].argmax()][0])
topmost = tuple(cnt[cnt[:, :, 1].argmin()][0])
bottommost = tuple(cnt[cnt[:, :, 1].argmax()][0])