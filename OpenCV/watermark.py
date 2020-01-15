import numpy as np
import cv2
from utils import CFEVideoConf, image_resize

cap = cv2.VideoCapture(0)

save_path = 'saved-media/watermark.mp4'
frames_per_second = 24
config = CFEVideoConf(cap, filepath=save_path, res='720p')
out = cv2.VideoWriter(save_path, config.video_type, frames_per_second, config.dims)

img_path = 'images/logo/wt.png'
logo = cv2.imread(img_path, -1)
watermark = image_resize(logo, height=50)
# watermark = cv2.cvtColor(watermark, cv2.COLOR_BGR2GRAY)
# watermark = cv2.cvtColor(watermark, cv2.COLOR_GRAY2BGR)
watermark = cv2.cvtColor(watermark, cv2.COLOR_BGR2BGRA)

# cv2.imshow('watermark', watermark)

while True:
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

    # print(frame[50, 150])
    # color = (255, 0, 0)
    # stroke = 2
    # start_cord_x = 50
    # start_cord_y = 150
    # w = 100
    # h = 100
    # end_cord_x = start_cord_x + w
    # end_cord_y = start_cord_y + h
    # cv2.rectangle(frame, (start_cord_x, start_cord_x), (end_cord_x, end_cord_y), color, stroke)
    # print(frame[start_cord_x:end_cord_x, start_cord_y:end_cord_y])
    # out.write(frame)

    frame_h, frame_w, frame_c = frame.shape
    # print(frame.shape)

    # overlay w/ 4 channels RGB and Alpha
    overlay = np.zeros((frame_h, frame_w, 4), dtype='uint8')

    # overlay[100:250, 100:125] = (255, 0, 0, 1)
    # overlay[100:250, 150:255] = (0, 255, 0, 1)
    # overlay[start_y:end_y, start_x:end_x] = (B, G, R, A)
    # cv2.imshow("overlay", overlay)

    watermark_h, watermark_w, watermark_c = watermark.shape
    for i in range(0, watermark_h):
        for j in range(0, watermark_w):
            if watermark[i, j][3] != 0:
                # watermark[i, j] # RGBA
                offset = 10
                h_offset = frame_h - watermark_h - offset
                w_offset = frame_w - watermark_w - offset
                overlay[h_offset + i, w_offset + j] = watermark[i, j]

    cv2.addWeighted(overlay, 0.25, frame, 1.0, 0, frame)

    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    out.write(frame)
    
    cv2.imshow('frame', frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()