import cv2
import numpy as np
from imutils import contours
from imutils.perspective import four_point_transform
import imutils


ANSWER_KEY = {
	0: 1,
	1: 4,
	2: 0,
	3: 3,
	4: 1
}

image = cv2.imread('images/arkusz.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(blurred, 75, 200)

cnts = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
docCnt = None

 # at least one contour was found
if len(cnts) > 0:
# descending order
	cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

	for c in cnts:
		# approximating contour
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02 * peri, True)

		# if approximated contour has four point,
		# assume, the paper is found
		if len(approx) == 4:
			docCnt = approx
			break
		
while True:
	cv2.imshow('frame', edged)

	if cv2.waitKey(20) & 0xFF == ord('q'):
		break

cv2.destroyAllWindows()