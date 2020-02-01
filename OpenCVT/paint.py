import cv2
import numpy as np

def nothing(x):
    pass

img = np.zeros((512, 512, 3), np.uint8)
cv2.namedWindow('img')
color = (255, 255, 255)
drawing = True


def draw(event, x, y, flags, param):
    global color, drawing
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        cv2.circle(img, (x, y), 5, color, -1)
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            cv2.circle(img, (x, y), 5, color, -1)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False


if __name__ == '__main__':
    cv2.createTrackbar('R', 'img', 0, 255, nothing)
    cv2.createTrackbar('G', 'img', 0, 255, nothing)
    cv2.createTrackbar('B', 'img', 0, 255, nothing)

    while True:
        cv2.setMouseCallback('img', draw)

        cv2.imshow('img', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        r = cv2.getTrackbarPos('R', 'img')
        g = cv2.getTrackbarPos('G', 'img')
        b = cv2.getTrackbarPos('B', 'img')

        color = (b,g,r)

    cv2.destroyAllWindows()