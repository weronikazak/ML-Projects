import cv2
import numpy as np
from imutils import contours
from imutils import perspective
import imutils
from scipy.spatial import distance as dist

OBJ_WIDTH = 20.0

def middle_point(A, B):
	AA = (A[0] + B[0]) * 0.5
	BB = (A[1] + B[1]) * 0.5
	return (AA, BB)

image = cv2.imread('images/objects.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (7, 7), 0)

edged = cv2.Canny(blurred, 50, 100)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)

cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

(cnts, _) = contours.sort_contours(cnts)
pixels_per_metric = None

for c in cnts:
	if cv2.contourArea(c) < 100:
		continue

	org = image.copy()
	box = cv2.minAreaRect(c)
	box = cv2.boxPoints(box)
	box = np.array(box, dtype="int")

	box = perspective.order_points(box)
	cv2.drawContours(org, [box.astype("int")], -1, (0, 255, 0), 2)

	for (x, y) in box:
		cv2.circle(org, (int(x), int(y)), 5, (0, 0, 255), -1)
		(tl, tr, br, bl) = box
		(tltrX, tltrY) = middle_point(tl, tr)
		(blbrX, blbrY) = middle_point(bl, br)

		(tlblX, tlblY) = middle_point(tl, bl)
		(trbrX, trbrY) = middle_point(tl, br)

		cv2.circle(org, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
		cv2.circle(org, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
		cv2.circle(org, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
		cv2.circle(org, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)

		cv2.line(org, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
					(255, 0, 0), 2)
		cv2.line(org, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
					(255, 0, 0), 2)

		dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
		dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

		if pixels_per_metric is None:
			pixels_per_metric = dB / OBJ_WIDTH

		dimA = dA / pixels_per_metric
		dimB = dB / pixels_per_metric

		cv2.putText(org, "{:.1f}in".format(dimA), (int(tltrX - 15), int(tltrY - 10)),
					cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)

		cv2.putText(org, "{:.1f}in".format(dimB), (int(trbrX + 10), int(trbrY)),
					cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)

		cv2.imshow("img", org)

		cv2.waitKey(0)

# src = https://www.pyimagesearch.com/2016/03/28/measuring-size-of-objects-in-an-image-with-opencv/