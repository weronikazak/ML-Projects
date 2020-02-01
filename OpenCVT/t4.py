# events, mouse as a paint-brush
import cv2
import numpy as np

# shows all the available events provided by cv2
# available_events = [i for i in dir(cv2) if 'EVENT' in i]
# print(available_events)

# draw on double-click
def draw_circle(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(img, (x, y), 100, (255, 0, 0), -1)


def demo():
    cv2.setMouseCallback('img', draw_circle)

    while True:
        cv2.imshow('img', img)
        if cv2.waitKey(20) & 0xFF == ord("q"):
            break


# ---------------------
# MORE ADVANCED VERSION
# ---------------------

drawing = False # if mouse is pressed
mode = True # if True, draw rectngle. Toggling on 'm'
ix, iy = -1, -1
img = np.zeros((512, 512, 3), np.uint8)
cv2.namedWindow('img')

def draw_circle_adv(event, x, y, flags, param):
    global ix, iy, drawing, mode

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            if mode == True:
                cv2.rectangle(img, (ix, iy), (x, y), (0, 255, 255), -1)
            else:
                cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        if mode == True:
            cv2.rectangle(img, (ix, iy), (x, y), (255 ,0,0), -1)
        else:
            cv2.circle(img, (x, y), 5, (0, 0, 255), -1)


def adv():
    global mode
    cv2.setMouseCallback('img', draw_circle_adv)

    while True:
        cv2.imshow('img', img)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('m'):
            mode = not mode
        elif k == ord('q'):
            break

if __name__ == "__main__":
    adv()
    cv2.destroyAllWindows()