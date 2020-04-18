import cv2
import os
import tensorflow as tf
from PIL import Image
import numpy as np

camera = cv2.VideoCapture(0)

def image_to_numpy(img):
    (width, height) = img.size
    return np.array(img.getdata()).reshape(width, height, 3).astype(np.uint8)

