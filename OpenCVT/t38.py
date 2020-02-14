# background substraction
import numpy as np
import cv2
import matplotlib.pyplot as plt

cap = cv2.VideoCapture('images/cars.mp4')

# ------------------------
# BackgroundSubstractorMOG
# ------------------------
# uses gaussian mixture-based background-foreground
# segmentation algorithm
# shadow param

fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()

# --------------------------
# BakcgroundSubstractionMOG2
# --------------------------
# same as above BUT slects the appropriate number of gaussian
# distrubution of each pixel. provides better adaptibility
# shadow param

fgbg1 = cv2.createBackgroundSubtractorMOG2()

# ------------------------
# BackgroundSubstractorGMG
# ------------------------
# combines statistical background image estimation and bayesian segmentation
# black window during first few fraes

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
fgbg2 = cv2.bgsegm.createBackgroundSubtractorGMG()

while True:
    ret, frame = cap.read()

    fgmask = fgbg.apply(frame.copy())
    fgmask1 = fgbg1.apply(frame.copy())
    fgmask2 = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

    cv2.imshow('frame', fgmask)
    cv2.imshow('frame1', fgmask1)
    cv2.imshow('frame2', fgmask2)

    if cv2.waitKey(20) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()