import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt

data = keras.datasets.fashion_mnist

(train_images, train_labels), (test_images, test_labels) = data.load_data()

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
                'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']


train_images = train_images/255.0
train_labels = train_labels/255.0 # to get the decimal/float values

plt.imshow(train_images[7], cmap=plt)
plt.show()
# print(train_labels[6])