import tensorflow as tf
import IPython.display as display
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import PIL.Image
import time
import functools
import cv2

mpl.rcParams['figure.figsize'] = (12, 12)
mpl.rcParams['axes.grid'] = False

def tensor_to_image(tensor):
    tensor = tensor * 255
    tensor = np.array(tensor, dtype=np.uint8)
    if np.ndim(tensor) > 3:
        assert tensor.shape[0] == 1 # if condition returns False, AssertionError is raised
        tensor = tensor[0]
    return PIL.Image.fromarray(tensor)

img_path = cv2.imread('images/girl.jpg')
style_path = cv2.imread('images/style.jpg')

def load_img(path):
    max_dim = 512
    img = tf.io.read_file(path)
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)

    shape = tf.cast(tf.shape(img)[:-1], tf.float32)
    long_dim = max(shape)
    scale = max_dim / long_dim

    new_shape = tf.cast(shape * scale, tf.int32)

    img = tf.image.resize(img, new_shape)
    img = img[tf.newaxis, :]
    return img

def display_img(image, title=None):
    if len(image.shape) > 3:
        image = tf.squeeze(image, axis=3)

    plt.imshow(image)
    if title:
        plt.title(title)


content_img = load_img(img_path)
style_img = load_img(style_path)