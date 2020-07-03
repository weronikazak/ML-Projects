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

paper = four_point_transform(image, docCnt.reshape(4, 2))
warped = four_point_transform(gray, docCnt.reshape(4, 2))

thresh = cv2.threshold(warped, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
questionsCnts = []

for c in cnts:
	(x, y, w, h) = cv2.boundingRect(c)
	ar = w / float(h)

	# region should be sufficiently wide, tall and have
	# an aspect ratio approximately equal to 1
	if w >= 20 and h >= 20 and ar >= 0.9 and ar <= 1.1:
		questionsCnts.append(c)
		
# sort contours top-t-bottom, then initialize
# total number of correct answers
questionsCnts = contours.sort_contours(questionsCnts,
	method="top-to-bottom")[0]
correct = 0


for (q, i) in enumerate(cnts):
	mask = np.zeros(thresh.shape, dtype="uint8")
	cv2.drawContours(mask, [c], -1, 255, -1)

	for (j, c) in enumerate(cnts):
		mask = np.zeros(thresh.shape, dtype="uint8")
		cv2.drawContours(mask, [c], -1, 255, -1)

		mask = cv2.bitwise_and(thresh, thresh, mask=mask)
		total = cv2.countNonZero(mask)


		if bubbled is None or total > bubbled[0]:
			bubbled = (total, j)

	color = (0, 0, 255)
	k = ANSWER_KEY[q]

	if k == bubbled[1]:
		color = (0, 255, 0)
		correct += 1

	cv2.drawContours(paper, [cnts[k]], -1, color, 3)
score = (correct / 5.) * 100
cv2.putText(paper, score, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

while True:
	cv2.imshow('frame', paper)

	if cv2.waitKey(20) & 0xFF == ord('q'):
		break

cv2.destroyAllWindows()