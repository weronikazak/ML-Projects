import cv2
import numpy as np

x = np.uint8([250])
y = np.uint8([10])

# -----------------
#  IMAGE ADDITION
# -----------------


# CV2 img addition
print(cv2.add(x, y)) # 250 + 10 = 260 => 255
# NumPy img addition
print(x + y)         # 250 + 10 = 26- % 256 = 4


# -----------------
#    IMAGE BLUR
# -----------------

img1 = cv2.imread('img.jpg')
img2 = cv2.imread('img1.jpg')

dst = cv2.addWeighted(img1, 0.7, img2, 0.3, 0)

cv2.imshow('dst', dst)
cv2.waitKey(0)
cv2.destroyAllWindows()
