import cv2
import numpy as np
from imutils import contours
from imutils.perspective import four_point_transform
import imutils
import time

camera = cv2.VideoCapture(0)
camera.set(3, 1280)
camera.set(3, 720)

cv2.namedWindow("frame", cv2.WINDOW_NORMAL)

pen_img = cv2.resize(cv2.imread('images/pen.jpg', 1), (100, 100))
eraser_img = cv2.resize(cv2.imread('images/eraser.jpg', 1), (100, 100))

background_threshold = 200
background_object = cv2.createBackgroundSubtractorMOG2(detectShadows=False)

switch = "Pen"

last_switch = time.time()

kernel = np.ones((5, 5), np.uint8)

load_from_disk = True

if load_from_disk:
	penval = np.load('penval.npy')

noiseth = 800

canvas = None
x1, y1 = 0, 0

# threshold for wiper, the size of the contour must be bigger
wiperth = 40000
clear = False

while True:
	ret, frame = camera.read()
	if not ret: break

	frame = cv2.flip(frame, 1)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	if canvas is None:
		canvas = np.zeros_like(frame)

	# apply the bcgrd substractor to top left of the frame
	top_left = frame[0:100, 0:100]
	fgmask = background_object.apply(top_left)

	# note the number of pixels that are white as lvl of discruption
	switch_thresh = np.sum(fgmask==255)

	# if th discruption is greater than background thresh and tere has been
	# some time after the previous switch, then can change the obj type
	if switch_thresh > background_threshold and (time.time()-last_switch) > 1:
		last_switch = time.time()

		if switch == "Pen":
			switch = "Eraser"
		else:
			switch = "Pen"

	if load_from_disk:
		lower_range = penval[0]
		upper_range = penval[1]
	else:
		lower_range = np.array([143, 139, 0])
		upper_range = np.array([179, 255, 255])

	# filter the image and get the binary mask, where white
	# represents target colour
	mask = cv2.inRange(hsv, lower_range, upper_range)

	mask = cv2.erode(mask, kernel, iterations=1)
	mask = cv2.dilate(mask, kernel, iterations=2)

	contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL,
											cv2.CHAIN_APPROX_SIMPLE)

	# make sure there is contour present and also make sure
	# its size is bigger than noise threshold
	if contours and cv2.contourArea(max(contours, key=cv2.contourArea)) > noiseth:
		c = max(contours, key=cv2.contourArea)
		area = cv2.contourArea(c)

		x2, y2, w, h = cv2.boundingRect(c)

		if x1 == 0 and y1 == 0:
			x1, y1 = x2, y2
		else:
			if switch == "Pen":
				canvas = cv2.line(canvas, (x1, y2), (x1, y2), [255, 0, 0], 5)
			else:
				cv2.circle(canvas, (x2, y2), 20, (0, 0, 0), -1)
		x1, y1 = x2, y2

	# if area is greater than the wiper threshold, then set the var
	# clear and warn user
		if area > wiperth:
			cv2.putText(canvas, "Clearing canvas", (100, 200), cv2.FONT_HERSHEY_SIMPLEX,
							2, (0, 0, 255), 5, cv2.LINE_AA)
			clear = True

	else:
		# if no contour detected
		x1, y1 = 0, 0

	_, mask = cv2.threshold(cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY), 20, 255,
				cv2.THRESH_BINARY)
	foreground = cv2.bitwise_and(canvas, canvas, mask=mask)
	background = cv2.bitwise_and(frame, frame, mask=cv2.bitwise_not(mask))
	frame = cv2.add(foreground, background)

	if switch != "Pen":
		cv2.circle(frame, (x1, y1), 20, (255, 255, 255), -1)
		frame[0:100, 0:100] = eraser_img
	else:
		frame[0:100, 0:100] = pen_img


	cv2.imshow('frame', frame)

	if cv2.waitKey(20) & 0xFF == ord('q'):
		break

	if clear:
		time.sleep(1)
		canvas = None

		clear = False


camera.release()
cv2.destroyAllWindows()

# src https://www.learnopencv.com/creating-a-virtual-pen-and-eraser-with-opencv/?ck_subscriber_id=760660522