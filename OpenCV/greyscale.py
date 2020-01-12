import cv2
import numpy as np

cap = cv2.VideoCapture(0)


while True:
    # capture frame by frame
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    cv2.imshow('frame', frame)
    cv2.imshow('gray', gray)

    if cv2.waitKey(20) & 0xFF == ord("q"):
        break