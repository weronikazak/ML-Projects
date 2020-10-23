import cv2
import numpy as np


camera = cv2.VideoCapture(0)
dimensions = (1280, 720)

camera.set(3, dimensions[0])
camera.set(4, dimensions[1])

frames_per_seconds = 21.0
video_type_cv2 = cv2.VideoWriter_fourcc(*'XVID')

out = cv2.VideoWriter("video.mp4", video_type_cv2, frames_per_seconds, dimensions)

while True:
	ret, frame = camera.read()
	out.write(frame)

	cv2.imshow("frame", frame)

	if cv2.waitKey(20) & 0xFF == ord("q"):
		break

camera.release()
out.release()
cv2.destroyAllWindows()