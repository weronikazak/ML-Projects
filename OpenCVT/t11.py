# colourspaces, object tracking
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()

    # convert to HSV - Hue Saturation Value
    # hue: 0 - 359
    # sat: 0 - 100
    # val: 0 - 100
    hvs =cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # defining range of blue colour in HSV
    lower_blue = np.array([0, 150, 50])
    upper_blue = np.array([20, 255, 255])

    # thresholding the HSV image to get only blue colour
    mask = cv2.inRange(hvs, lower_blue, upper_blue)

    # bitwise AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('res', res)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

# FINDING HSV VALUES
# green = np.uint8([[[0, 255, 0]]])
# hsv_green = cv2.cvtColor(green, cv2.COLOR_BGR2HSV)
# print(hsv_green)
# [[[ 60 255 255]]]
# for the function above you both add and substract from the first value 10