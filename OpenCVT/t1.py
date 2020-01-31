# reading and writing an image using cv2 or matplotlib
import cv2
import numpy as np
from matplotlib import pyplot as plt

def plain_cv2(img):
    cv2.imshow('image', img)
    cv2.imwrite('redhead.png', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def matplot(img):
    plt.imshow(img, cmap='gray', interpolation='bicubic')
    plt.xticks([])
    plt.yticks([])
    plt.show()

if __name__ == "__main__":
    img = cv2.imread('img.jpg', 0)

    matplot(img)