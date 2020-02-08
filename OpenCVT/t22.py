# TEMPLATE MATCHING
import cv2
import numpy as np
from matplotlib import pyplot as plt

# ------------------------------------
# TEMPLATE MATCHING WITH SINGLE OBJECT
# ------------------------------------

img = cv2.imread('images/img1.jpg', 0)
img2 = img.copy()
template = cv2.imread('images/template.jpg', 0)
w, h = template.shape[::-1]

methods = [
        'cv2.TM_CCOEFF',
        'cv2.TM_CCOEFF_NORMED',
        'cv2.TM_CCORR',
        'cv2.TM_CCORR_NORMED',
        'cv2.TM_SQDIFF',
        'cv2.TM_SQDIFF_NORMED'
]

for meth in methods:
    img = img2.copy()
    method = eval(meth)

    # apply template matching
    res = cv2.matchTemplate(img, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # if method is TM_SQDIFF(..) take minimum
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    cv2.rectangle(img, top_left, bottom_right, 255, 2)

    plt.subplot(121)
    plt.imshow(res, cmap='gray')
    plt.title('Matching result')
    plt.xticks([])
    plt.yticks([])
    
    plt.subplot(122)
    plt.imshow(img, cmap='gray')
    plt.title('Detected point')
    plt.xticks([])
    plt.yticks([])
    
    plt.suptitle(meth)

    plt.show()
    

# ----------------------------------------
# TEMPLATE MATCHING WITH MULTIPLE OBJECTS
# ----------------------------------------

img_rgb = cv2.imread('images/mario.jpg')
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
template = cv2.imread('images/coin.jpg', 0)
w, h = template.shape[::-1]

res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
threshold = 0.8
loc = np.where( res >= threshold )
for pt in zip(*loc[::-1]):
    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + g), (0, 0, 255), 2)

cv2.imwrite('images/res.png', img_rgb)