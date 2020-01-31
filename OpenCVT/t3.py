# events, mouse as a paint-brush
import cv2
import numpy as np

# shows all the available events provided by cv2
# available_events = [i for i in dir(cv2) if 'EVENT' in i]
# print(available_events)

def draw_circle(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(img, (x, y), 100, (255, 0, 0), -1)

# create a black image, a window and bind the function to window
img = np.zeros((512, 512, 3), np.uint8)
# 0 - 3: white and black
# 3 - 4: colour
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_circle)

while True:
    cv2.imshow('image', img)
    if cv2.waitKey(20) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()