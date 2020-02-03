import cv2
from matplotlib import pyplot as plt
import random

im_gray = cv2.imread('images/emilia-clarke/1.jpg', cv2.IMREAD_GRAYSCALE)

filters = [
    cv2.COLORMAP_AUTUMN,
    cv2.COLORMAP_BONE,
    cv2.COLORMAP_JET,
    cv2.COLORMAP_WINTER,
    cv2.COLORMAP_RAINBOW,
    cv2.COLORMAP_OCEAN,
    cv2.COLORMAP_SUMMER,
    cv2.COLORMAP_SPRING,
    cv2.COLORMAP_COOL,
    cv2.COLORMAP_HSV,
    cv2.COLORMAP_PINK,
    cv2.COLORMAP_HOT,
    cv2.COLORMAP_PARULA,
    cv2.COLORMAP_MAGMA,
    cv2.COLORMAP_INFERNO,
    cv2.COLORMAP_PLASMA,
    cv2.COLORMAP_VIRIDIS,
    cv2.COLORMAP_CIVIDIS,
    cv2.COLORMAP_TWILIGHT,
    cv2.COLORMAP_TWILIGHT_SHIFTED,
    cv2.COLORMAP_TURBO
    ]

im_color = cv2.applyColorMap(im_gray, random.choice(filters))

cv2.imshow('color', im_color)
cv2.waitKey(0)
cv2.destroyAllWindows()

# creating own
# im_color2 = cv2.LUT(im_gray.copy(), lut)