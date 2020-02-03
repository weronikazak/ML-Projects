import cv2

src = cv2.imread("threshold.png", cv2.IMREAD_GRAYSCALE)
# img2gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

# thresh 0 - all contasted
# thresh 127 - 3 gone
thresh = 127

# maxVal 128 - sets the value of thresholded img to 128
max_value = 255

# standard - white on black
th, dst = cv2.threshold(src, thresh, max_value, cv2.THRESH_BINARY)
# inverse - black on white
in_th, in_dst = cv2.threshold(src, thresh, max_value, cv2.THRESH_BINARY_INV)
# all values above threshold (127), are set to threshold (127). less values are unchanged
th_th, th_dst = cv2.threshold(src, thresh, max_value, cv2.THRESH_TRUNC)
# if the pixel value is lesser than threshold it's set to zero. maxval is ignored
z_th, z_dst = cv2.threshold(src, thresh, max_value, cv2.THRESH_TOZERO)
# inverted zero. if pixel is greater than threshold, maxVal is ignored
zi_th, zi_dst = cv2.threshold(src, thresh, max_value, cv2.THRESH_TOZERO_INV)


cv2.imshow('dst', dst)
cv2.imshow('inverse', in_dst)
cv2.imshow('trunc', th_dst)
cv2.imshow('zero', z_dst)
cv2.imshow('zero inverse', zi_dst)
cv2.waitKey(0)
cv2.destroyAllWindows()