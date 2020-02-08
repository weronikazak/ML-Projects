# więcej funkcji konturów
import cv2
import numpy as np

img = cv2.imread('images/img.jpg', 0)
ret, thresh = cv2.threshold(img, 127, 255, 0)
contours, hierarchy = cv2.findContours(thresh, 1, 2)

cnt = contours[0]

# -----------------
# CONVEXITY DEFECTS
# -----------------
# wada wypukła - każde odchylenie convex hulla
# zwraca tablice o wyglądzie
# [star_point, end_point, farthest_point, approximate_distance_to_farthest_point]
hull = cv2.convexHull(cnt, returnPoints=False)
defects = cv2.convexityDefects(cnt, hull)

for i in range(defects.shape[0]):
    s, e, f, d = defects[i, 0]
    start = tuple(cnt[s][0])
    end = tuple(cnt[e][0])
    far = tuple(cnt[e][0])
    cv2.line(img, start, far, [0, 255, 0], 2)
    cv2.circle(img, far, 5, [0, 0, 255], -1)

cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()


# ------------------
# POINT POLYGON TEST
# ------------------
# znajduje najkrótszy dystans między punktem na obrazie i konturem
# zwraca negatywną, jeśli punkt jest poza konturem, pozytywną, kiedy w środku
# i 0 jeśli jest na konturze
dist = cv2.pointPolygonTest(cnt, (50, 50), True)
# trzeci argument to measureDist.
# jeśli jest True znajduje dystans, jeśli False zwraca -1, +1, 0 (patrz wyżej)

# -------------
# MATCH SHAPES
# -------------

img1 = cv2.imread('images/star1.jpg')
img2 = cv2.imread('images/star2.jpg')
ret, thresh1 = cv2.threshold(img1, 127, 255, 0)
ret, thresh2 = cv2.threshold(img2, 127, 255, 0)
contours, hierarchy = cv2.findContours(thresh1, 2, 1)
cnt1 = contours[0]
contours, hierarchy = cv2.findContours(thresh2, 2, 1)
cnt2 = contours[0]

ret = cv2.matchShapes(cnt1, cnt2, 1, 0.0)

print(ret)