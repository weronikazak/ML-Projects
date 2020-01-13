import cv2
import numpy as np
import os


filename = 'video.avi'
frames_per_seconds = 24.0
my_res = '720p'


# Standard Video Dimensions Sizes
STD_DIMENSTIONS = {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160)
}

# VIDEO ENCODING
VIDEO_TYPES = {
    'avi': cv2.VideoWriter_fourcc(*'XVID'),
    'mp4': cv2.VideoWriter_fourcc(*'XVID'),
}

def change_res(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)

def get_dims(cap, res='1080p'):
    width, height = STD_DIMENSTIONS['480p']
    if res in STD_DIMENSTIONS:
        width, height = STD_DIMENSTIONS[res]
    change_res(cap, width, height)
    return width, height

def get_video_type(filename):
    filename, ext = os.path.splitext(filename)
    if ext in VIDEO_TYPES:
        return VIDEO_TYPES[ext]
    return VIDEO_TYPES['avi']


cap = cv2.VideoCapture(0)
dims = get_dims(cap, res=my_res)
video_type_cv2 = get_video_type(filename)

out = cv2.VideoWriter(filename, video_type_cv2, frames_per_seconds, dims)

while True:
    # capture frame by frame
    ret, frame = cap.read()
    out.write(frame)

    cv2.imshow('frame', frame)

    if cv2.waitKey(20) & 0xFF == ord("q"):
        break

cap.release()
out.release()
cv2.destroyAllWindows()