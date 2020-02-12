# Feature Matching
import cv2
import numpy as np
import matplotlib.pyplot as plt

img1 = cv2.imread('images/beer.jpg', 0)
img2 = cv2.imread('images/beer_copy.jpg', 0)

# -----------------------------
# BRURE-FORCE MATCHING WITH ORB
# -----------------------------

# initiate SIFT detector
orb = cv2.ORB_create()

# find the keypooints and descriptors with SIFT
kp1, des1 = orb.detectAndCompute(img1, None)
kp2, des2 = orb.detectAndCompute(img2, None)

# create BFMatch object
bf = cv2.BFMatcher_create(cv2.NORM_HAMMING, crossCheck=True)

# match descriptors
matches = bf.match(des1, des2)

# sort them in the order of their distance
matches = sorted(matches, key= lambda x: x.distance)

# draw first 10 matches
img3 = cv2.drawMatches(img1, kp1,img2, kp2, matches[:10], None, flags=2)

plt.imshow(img3)
plt.show()

# ------------------------------
# BRUTE-FORCE MATCHING WITH SIFT
# ------------------------------

sift = cv2.xfeatures2d.SIFT_create()

kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)

matches = bf.knnMatch(des1, des2, k=2)

# apply ratio test
good = []
for m, n in matches:
    if m.distance < 0.75*n.distance:
        good.append([m])

img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good, None, flags=2)

plt.show(img3)
plt.show()