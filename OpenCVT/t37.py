# OPTICAL FLOW
import numpy as np
import cv2

# przepływ optyczny (optical form) to wzór pozornego ruchu obiektów
# obrazu między dwiema kolejnymi ramkami spowodowanego ruchem obiektu
# lub kamery. To pole wektorowe 2D w którym mkażdy wektor jest wektorem 
# przemieszczenia pokazującym ruch punktów z pierwszej klatki do drugiej
# zastosowanie:
# Structure from Motion
# Video Compression
# Video Stabilization

# warunki:
# intensywnosc pikseli obiektu nie zmienia sie miedzy kolejnymi klatkami
# sasiadujace piksele maja podobny ruch (motion)

# -------------------------
# LUCAS-KANADE OPTICAL FLOW
# -------------------------

cap = cv2.VideoCapture('images/cars.mp4')

# params for ShiThmasi corner detection
feature_params = dict(  maxCorners = 100,
                        qualityLevel=0.3,
                        minDistance = 7,
                        blockSize = 7)

# params dor Lucas kanade oplical flow
lk_params = dict( winSize = (15, 15),
                    maxLevel = 2,
                    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.3))

color = np.random.randint(0, 255, (100, 3))

# take first frame and find corners in it
ret, old_frame = cap.read()
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)

# create a mask image for drawing purposes
mask = np.zeros_like(old_frame)

while True:
    ret, frame = cap.read()
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # calculate optical flow
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

    # select good points
    good_new = p1[st==1]
    good_old = p0[st==1]

    # draw the tracks
    for i, (new, old) in enumerate(zip(good_new, good_old)):
        a, b = new.ravel()
        c, d = old.ravel()
        mask = cv2.line(mask, (a, b), (c, d), color[i].tolist(), 2)
        frame = cv2.circle(frame, (a, b), 5, color[i].tolist(),-1)
    
    img = cv2.add(frame, mask)

    cv2.imshow("frame", img)

    if cv2.waitKey(30) & 0xFF == ord("q"):
        break
    
    old_gray = frame_gray.copy()
    p0 = good_new.reshape(-1,1,2)

cv2.destroyAllWindows()
cap.release()

# kod nie sprawdza jak poprawne są następne keypoints. czyli nawet jeśli punkt
# elementu zniknie na obrazie, istnieje szansa, że optical flow znajdzie
# następny punkt, który może wyglądać podobnie.

# --------------------
# DESNSE OPTICAL FLOW
# --------------------

cap = cv2.VideoCapture('images/cars.mp4')
ret, frame1 = cap.read()
prvs = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
hsv = np.zeros_like(frame1)
hsv[...,1] = 255

while True:
    ret, frame2 = cap.read()
    next = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    flow = cv2.calcOpticalFlowFarneback(prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)

    mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
    hsv[...,0] = ang*180/np.pi/2
    hsv[...,2] = cv2.normalize(mag, None, 0, 255,cv2.NORM_MINMAX)
    rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    cv2.imshow("frame2", rgb)
    k = cv2.waitKey(30) & 0xff

    if k == ord('q'):
        break
    elif k == ord('s'):
        cv2.imwrite('optical.fb.png', frame2)
        cv2.imwrite('opticalhsv.png', rgb)
    prvs = next

cap.release()
cv2.destroyAllWindows()
