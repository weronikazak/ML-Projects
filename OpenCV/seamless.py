import cv2
import numpy as np

# cv2.seamlessClone(src, dst, mask, center, flags)
# src - source, that will be cloned into des (airplane)
# dst - destination image into which the src will be cloned (sky)
# mask - mask around all objects to clone. should be the image size
# center - location of center of src in des
# flags - flags, here its NORMAL_CLONE and MIXED_CLONE

src = cv2.imread('images/plane.jpg')
dst = cv2.imread('images/sky.jpg')

src_mask = np.zeros(src.shape, src.dtype)
poly = np.array([ [4, 80], [30, 54], [151, 63], [254, 37], [298, 90], [272, 134], [43, 122]], np.int32)
cv2.fillPoly(src_mask, [poly], (255, 255, 255))

center = (800, 100)

output = cv2.seamlessClone(src, dst, src_mask, center, cv2.NORMAL_CLONE)

cv2.imwrite('images/seamless.jpg', output)



im = cv2.imread('images/wood.jpg')
obj = cv2.imread('images/text.jpg')

# all white mask
mask = 255 * np.ones(obj.shape, obj.dtype)

# look for the center of img
width, height, channels = im.shape
center = (int(height/2), int(width/2))

normal_clone = cv2.seamlessClone(obj, im, mask, center, cv2.NORMAL_CLONE)
mixed_clone = cv2.seamlessClone(obj, im, mask, center, cv2.MIXED_CLONE)

cv2.imwrite('images/normal_clone.jpg', normal_clone)
cv2.imwrite('images/mixed_clone.jpg', mixed_clone)



# TUTORIAL: