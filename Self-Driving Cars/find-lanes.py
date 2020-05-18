import cv2
import numpy as np

def make_coords(img, line_params):
	slope, intercept = line_params
	y1 = img.shape[0]
	y2 = int(y1*(3/5))
	x1 = int((y1 - intercept)/slope)
	x2 = int((y2 - intercept)/slope)
	return np.array([x1, y1, x22, y2])


def canny(img):
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	blur = cv2.GaussianBlur(gray, (5, 5), 0)
	canny = cv2.Canny(blur, 50, 150)
	return canny

def region_of_interest(img):
	w, h = img.shape[:2]
	polygons = np.array([
		[(200, h), (1100, h), (550, 250)]])
	mask = np.zeros_like(img)
	cv2.fillPoly(mask, polygons, 255)
	masked_img = cv2.bitwise_and(img, mask)
	return masked_img


def display_lines(img, lines):
	line_image = np.zeros_like(img)
	if lines is not None:
		for line in lines:
			x1, y1, x2, y2 = line.reshape(4)
			cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
	return line_image


def avg_slope_intercept(img, lines):
	left_fit = []
	right_fit = []
	for line in lines:
		x1, y1, x2, y2 = line.reshape(4)
		parameters = np.polyfit((x1, x2), (y1, y2), 1)
		slope = parameters[0]
		intercept = parameters[1]
		if slope < 0:
			left_fit.append((slope, intercept))
		else:
			right_fit.append((slope, intercept))
	left_fit_avg = np.average(left_fit, axis=0)
	right_fit_avg = np.average(right_fit, axis=0)
	left_line = make_coords(img, left_fit_avg)
	right_line - make_coords(img, right_fit_avg)
	return np.array([left_line, right_line])



img = cv2.imread("images/test_image.jpg")

lane_img = np.copy(img)
canny_img = canny(lane_img)
cropped_img = region_of_interest(canny_img)
lines = cv2.HoughLinesP(cropped_img, 2, np.pi/100, 100,
	np.array([]), minLineLength=40, maxLineGap=5)
avg_lines = avg_slope_intercept(lane_img, lines)
line_img = display_lines(lane_img, lines)
combo_img = cv2.addWeighted(lane_img, 0.8, line_img, 1, 1 )


cv2.imshow("results", combo_img)
cv2.waitKey(0)

# src https://www.youtube.com/watch?v=eLTLtUVuuy4