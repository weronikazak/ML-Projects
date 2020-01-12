import cv2
import numpy as np

cap = cv2.VideoCapture(0)

def make_1080p():
    cap.set(3, 1920)
    cap.set(4, 1080)

def make_720p():
    cap.set(3, 1920)
    cap.set(4, 1080)

def make_480p():
    cap.set(3, 1920)
    cap.set(4, 1080)

def change_resolution(width, height):
    cap.set(3, width)
    cap.set(4, height)

def rescale_frame(frame, percent=75):
    scale_percent = 75
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

while True:
    ret, frame = cap.read()
    frame = rescale_frame(frame, percent=30)
    cv2.imshow('frame', frame)

    frame2 = rescale_frame(frame, percent=500)
    cv2.imshow('frame2', frame2)

    if cv2.waitKey(20) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()