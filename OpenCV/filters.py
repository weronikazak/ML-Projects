from utils import CFEVideoConf, image_resize
import glob
import math
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

frames_per_second = 20
save_path = 'saved-media/filter.mp4'
config = CFEVideoConf(cap, save_path, res='480p')
# out = cv2.VideoWriter(save_path, config.video_type, frames_per_second, config.dims)


def apply_invert(frame):
    return cv2.bitwise_not(frame)


def verify_alpha_channel(frame):
    try:
        frame.shape[3] # 4th position
    except IndexError:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    return frame


def appy_color_overlay(frame,
                        intensity=0.5,
                        blue = 20,
                        green = 66,
                        red = 112):
                        
    frame = verify_alpha_channel(frame)
    frame_h, frame_w, frame_c = frame.shape
    color_bgra = (blue, green, red, 1)
    overlay = np.full((frame_h, frame_w, 4), color_bgra, dtype='uint8')
    cv2.addWeighted(overlay, intensity, frame, 1.0, 0, frame)

    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    return frame



def appy_sepia(frame, intensity=0.5):
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    # frame_h, frame_w, frame_c = frame.shape
    blue = 20
    green = 66
    red = 112
    frame = appy_color_overlay(frame, intensity, blue, green, red)
    # sepia_bgra = (blue, green, red, 1)
    # overlay = np.full((frame_h, frame_w, 4), sepia_bgra, dtype='uint8')
    # cv2.addWeighted(overlay, intensity, frame, 1.0, 0, frame)
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    return frame

def alpha_blend(frame_1, frame_2, mask):
    alpha = mask / 255.0
    blended = cv2.convertScaleAbs(frame_1*(1-alpha) + frame_2*alpha)
    return blended

def apply_circle_focus_blur(frame, intensity=0.2):
    frame = verify_alpha_channel(frame)
    frame_h, frame_w, frame_c = frame.shape
    y = int(frame_h/2)
    x = int(frame_w/2)
    center = (x, y)
    radius = int(x/2) # int(x/3)
    mask = np.zeros((frame_h, frame_w, 4), dtype='uint8')
    cv2.circle(mask, center, radius, (255, 255, 255), -1, cv2.LINE_AA)
    mask = cv2.GaussianBlur(mask, (21, 21), 11)
    blured = cv2.GaussianBlur(frame, (21, 21), 11)
    blended = alpha_blend(frame, blured, 255-mask)
    frame = cv2.cvtColor(blended, cv2.COLOR_BGRA2BGR)
    return frame


def apply_portrait_mode(frame):
    frame = verify_alpha_channel(frame)
    # cv2.imshow('frame', frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGRA)
    blured = cv2.GaussianBlur(frame, (21, 21), 11)
    blended = alpha_blend(frame, blured, mask)
    frame = cv2.cvtColor(blended, cv2.COLOR_BGRA2BGR)
    return frame


while True:
    # capture frame by frame
    ret, frame = cap.read()
    
    # invert = apply_invert(frame)
    # cv2.imshow('invert', invert)

    portrait_mode = apply_portrait_mode(frame)
    cv2.imshow('portrait', portrait_mode)

    # sepia = appy_sepia(frame.copy())
    # cv2.imshow('sepia', sepia)

    # circle_blur = apply_circle_focus_blur(frame.copy())
    # cv2.imshow('circle_blur', circle_blur)

    # blueish_color = appy_color_overlay(frame.copy(), 0.7, 200, 60, 30)
    # cv2.imshow('blueish', blueish_color)
    
    # cv2.imshow('frame', frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()