import cv2
import numpy as np
from imutils import contours
from imutils.perspective import four_point_transform
import imutils
import time

def nothing(x):
	pass

camera = cv2.VideoCapture(0)
camera.set(3, 1280)
camera.set(3, 720)

cv2.namedWindow("trackbars")

# HSV channels
# cv2.createTrackbar("L - H", "trackbars", 0, 179, nothing)
# cv2.createTrackbar("L - S", "trackbars", 0, 255, nothing)
# cv2.createTrackbar("L - V", "trackbars", 0, 255, nothing)
# cv2.createTrackbar("U - H", "trackbars", 179, 179, nothing)
# cv2.createTrackbar("U - S", "trackbars", 255, 255, nothing)
# cv2.createTrackbar("U - V", "trackbars", 255, 255, nothing)

load_from_disk = True

if load_from_disk:
	penval = np.load('penval.npy')

kernel = np.ones((5, 5), np.uint8)


while True:
	ret, frame = camera.read()
	if not ret: break

	frame = cv2.flip(frame, 1)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	if load_from_disk:
		lower_range = penval[0]
		upper_range = penval[1]
	else:
		lower_range = np.array([143, 139, 0])
		upper_range = np.array([179, 255, 255])

	# l_h = cv2.getTrackbarPos("L - H", "trackbars")
	# l_s = cv2.getTrackbarPos("L - S", "trackbars")
	# l_v = cv2.getTrackbarPos("L - V", "trackbars")
	# u_h = cv2.getTrackbarPos("U - H", "trackbars")
	# u_s = cv2.getTrackbarPos("U - S", "trackbars")
	# u_v = cv2.getTrackbarPos("U - V", "trackbars")



	# filter the image and get the binary mask, where white
	# represents target colour
	mask = cv2.inRange(hsv, lower_range, upper_range)

	mask = cv2.erode(mask, kernel, iterations=1)
	mask = cv2.dilate(mask, kernel, iterations=2)

	res = cv2.bitwise_and(frame, frame, mask=mask)

	mask_3 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

	# stack the mask, original frame and filteres result
	stacked = np.hstack((mask_3, frame, res))

	# show stacked frame at 0.4 0f the size
	cv2.imshow('trackbars', cv2.resize(stacked, None, fx=0.4, fy=0.4))

	if cv2.waitKey(20) & 0xFF == ord('q'):
		break

	if cv2.waitKey(20) & 0xFF == ord('s'):
		arr = [[l_h, l_s, l_v], [u_h, u_s, u_v]]
		print(arr)

		np.save('penval', arr)
		break
camera.release()
cv2.destroyAllWindows()