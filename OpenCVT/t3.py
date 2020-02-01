# lines, rectangles, polylines
import numpy as np
import cv2

img = np.zeros((512, 512, 3), np.uint8)

# drawing line
# arg2 - (x, y) poczatku linii, arg2 - (x, y) konca linii
cv2.line(img, (0, 100), (500, 500), (255, 0, 0), 5)


# drawing a rectangle
cv2.rectangle(img, (310, 20), (10, 280), (0, 255, 0), 3)

# drawing a circle
cv2.circle(img, (250, 250), 100, (0, 0, 255), 10)

# drawing an ellipse (połowa kółka)
cv2.ellipse(img, (300, 200), (100, 50), 0, 0, 180, 255, -1)

# drawing a polygon
# 1. coordinates of verticles.
points = np.array([[100, 500], [200, 30], [320, 400], [500, 100]], np.int32)
# 2. make into an array of shape ROWS x 1 x 2
# ROWS are number of verticles, it should be the type of int32
points = points.reshape((-1, 1, 2))
cv2.polylines(img, [points], False, (0, 255, 255))
# if False - idzie jako linia
# if True - łączy wszystkie punkty
# polinilii moze być kilka, niekoniecznie 4 punkty

points2 = np.array([[50, 500], [100, 400], [10, 300], [250, 100], [500, 10]], np.int32)
points2 = points2.reshape((-1 , 1, 2))
cv2.polylines(img, [points2], True, (255, 255, 0))

# drawing text
font = cv2.FONT_ITALIC
cv2.putText(img, "Siemanko", (-50, 500), font, 4, (255, 255, 255), 2, cv2.LINE_8)

cv2.imshow('img', img)

cv2.waitKey(0)
cv2.destroyAllWindows()