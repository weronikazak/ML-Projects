# INTERACTIVE FOREGROUND EXTRACTION
import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('images/img1.jpg')
mask = np.zeros(img.shape[:2], np.uint8)

bgModel = np.zeros((1, 65), np.float64)
fgModel = np.zeros((1, 65), np.float64)

newmask = cv2.imread('images/newmask.jpg', 0)

mask[newmask == 0] = 0
mask[newmask == 255] = 1
cv2.grabCut(img, mask, None, bgModel, fgModel, 5, cv2.GC_INIT_WITH_MASK)

# rect = (0, 0, 450, 450)
# cv2.grabCut(img, mask, rect, bgModel, fgModel, 5, cv2.GC_INIT_WITH_RECT)

mask2 = np.where((mask==2)|(mask==0), 0, 1).astype('uint8')
img = img*mask2[:, :, np.newaxis]

plt.imshow(img), plt.colorbar()
plt.show()