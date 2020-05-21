COCO = {
	0:  "nose",
	1:  "neck",
	2:  "r_shoulder",
	3:  "r_elbow",
	4:  "r_wrist",
	5:  "l_shoulder",
	6:  "l_elbow",
	7:  "l_wrist",
	8:  "r_hip",
	9:  "r_knee",
	10: "r_ankle",
	11: "l_hip",
	12: "l_knee",
	13: "l_ankle",
	14: "r_eye",
	15: "l_eye",
	16: "r_ear",
	17: "l_ear",
	18: "background"
}

MPII = {
	0:  "head",
	1:  "neck",
	2:  "r_shoulder",
	3:  "r_elbow",
	4:  "r_wrist",
	5:  "l_shoulder",
	6:  "l_elbow",
	7:  "l_wrist",
	8:  "r_hip",
	9:  "r_knee",
	10: "r_ankle",
	11: "l_hip",
	12: "l_knee",
	13: "l_ankle",
	14: "chest",
	15: "background"
}


import cv2
import numpy as np

protoFile = "data/pose_deploy_linevec_faster_4_stages.prototxt"
weightsFile = "data/pose_iter_160000.caffemodel"

net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)

frame = cv2.imread("images/photo.jpg")
frame_h, frame_w = frame.shape[:2]

input_h, input_w = 368, 368

innBlob = cv2.dnn.blobFromImage(frame, 1.0 / 255, (input_w, input_h),
			(0, 0, 0), swapRB=False, crop=False)

net.setInput(innBlob)

output = net.forward()
nPoints = 18


H, W = output.shape[2], output.shape[3]
points = []

for i in range(nPoints):
	probMap = output[0, i, :, :]

	minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)

	# scale the point to fir on the original img
	x = (frame_w * point[0]) / W
	y = (frame_h * point[1]) / H

	if prob > 0.1:
		cv2.circle(frame, (int(x), int(y)), 3, (0, 255, 255), thickness=-1,
				lineType=cv2.FILLED)
		cv2.putText(frame, f"{i}", (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX,
			1, (0, 0, 255), 3, lineType=cv2.LINE_AA)

		points.append((int(x), int(y)))
	else:
		points.append(None)

cv2.imshow("keypoints", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()