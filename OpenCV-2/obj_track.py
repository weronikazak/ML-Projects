import numpy as np
import os
import cv2
import imutils
import time
from collections import deque

camera = cv2.VideoCapture(0)

# green_u, green_l = (191, 29, 0), (255, 123, 6)
orange_u, orange_l = (52, 17, 14), (151, 73, 44)


time.sleep(2.)

pts = deque(maxlen=64)

while True:
    ret, frame = camera.read()

    if not ret: break

    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, orange_l, orange_u)
    mask = cv2.erode(mask, None, iterations=4)
    mask = cv2.dilate(mask, None, iterations=4)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        if radius > 40:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)

            cv2.circle(frame, center, 5, (0, 0, 255), -1)

    pts.appendleft(center)

    for i in range(1, len(pts)):
        if pts[i - 1] is None or pts[i] is None:
            continue
    
        thickness = int(np.sqrt(63 / float(i+1))* 2.5)
        cv2.line(frame, pts[i-1], pts[i], (0, 0, 255), thickness)

    cv2.imshow("frame", frame)

    if cv2.waitKey(20) & 0xFF == ord("q"):
        break


camera.release()
cv2.destroyAllWindows()
            


