import cv2
import imutils
import numpy as np
from sklearn.metrics import pairwise

bg = None

def runninig_average(image, aWeight):
    global bg

    if bg is None:
        bg = image.copy().astype("float")
        return

    cv2.accumulateWeighted(image, bg, aWeight)

def segment(image, threshold=25):
    global bg

    diff = cv2.absdiff(bg.astype("uint8"), image)

    thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)[1]

    contours, hierarchy = cv2.findContours(thresholded.copy(),
                        cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours) == 0:
        return
    else:
        segmented = max(contours, key=cv2.contourArea)
        return (thresholded, segmented)

        
def count(thresholded, segmented):
    chull = cv2.convexHull(segmented)

    ex_top = tuple(chull[chull[:, :, 1].argmin()][0])
    ex_bottom = tuple(chull[chull[:, :, 1].argmax()][0])
    ex_left = tuple(chull[chull[:, :, 0].argmin()][0])
    ex_right = tuple(chull[chull[:, :, 0].argmax()][0])

    center_X = int((ex_left[0] + ex_right[0]) / 2)
    center_Y = int((ex_top[1] + ex_bottom[1]) / 2)

    distance = pairwise.euclidean_distances([(center_X, center_Y)],
                Y=[ex_left, ex_right, ex_top, ex_bottom])[0]
    
    max_distance = distance[distance.argmax()]

    radius = int(0.8 * max_distance)

    circumference = (2 * np.pi * radius)

    circular_ROI = np.zeros(thresholded.shape[:2], dtype="uint8")

    cv2.circle(circular_ROI, (center_X, center_Y), radius, 255, 1)

    circular_ROI = cv2.bitwise_and(thresholded, thresholded,
                                    mask=circular_ROI)

    contours, _ = cv2.findContours(circular_ROI.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_NONE)

    count = 0

    for c in contours:
        x, y, w, h = cv2.boundingRect(c)

        if ((center_Y + (center_Y * .25)) > (y + h)) and ((circumference * .25) > c.shape[0]):
            count += 1

    return count


aWeight = .5
cap = cv2.VideoCapture(0)
top, right, bottom, left = 80, 350, 295, 590
num_frames = 0

while True:
    ret, frame = cap.read()
    # cv2.imshow(frame, 'frame')
    frame = imutils.resize(frame, width=700, height=700)
    frame = cv2.flip(frame, 1)
    clone = frame.copy()
    (height, width) = frame.shape[:2]
    roi = frame[top:bottom, right:left]

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7,7), 0)

    if num_frames < 30:
        runninig_average(gray, aWeight)
    else:
        hand = segment(gray)

        if hand is not None:
            (thresholded, segmented) = hand
            cv2.drawContours(clone, [segmented + (right, top)], -1, (0, 0, 255))
            fingers = count(thresholded, segmented)
            cv2.putText(clone, str(fingers), (70, 45), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 0, 255), 2)
            
            cv2.imshow("Thresholded", thresholded)

    cv2.rectangle(clone, (left, top), (right, bottom), (0, 255, 0), 2)

    num_frames += 1

    cv2.imshow("Video Feed", clone)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()

