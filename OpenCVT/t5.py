# trackbars
import cv2
import numpy as np

def nothing(x):
    pass

img = np.zeros((300, 512, 3), np.uint8)
cv2.namedWindow('img')

# create trackbar
cv2.createTrackbar('R', 'img', 0, 255, nothing)
cv2.createTrackbar('G', 'img', 0, 255, nothing)
cv2.createTrackbar('B', 'img', 0, 255, nothing)

# switch for ON/OFF func
switch = '0: OFF \n1 : ON'
cv2.createTrackbar(switch, 'img', 0, 1, nothing)

while True:
    cv2.imshow('img', img)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'):
        break

    # get current positions of four trackers
    r = cv2.getTrackbarPos('R', 'img')
    g = cv2.getTrackbarPos('G', 'img')
    b = cv2.getTrackbarPos('B', 'img')
    s = cv2.getTrackbarPos('S', 'img')

    if s == 0:
        img[:] = 0
    else:
        img[:] = [b, g, r]

cv2.destroyAllWindows()