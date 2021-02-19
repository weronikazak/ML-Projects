import matplotlib.pyplot as plt
import numpy as np
import sklearn
import tensorflow.compat.v1 as tf
import scipy
import scipy.io
import scipy.misc
import imageio
import PIL
from PIL import Image
import os
import sys

def variable(value, dtype="float32", name=None):
	v = tf.Variable(bp.asarray(value, dtype=dtype), name=name)
	_get_session().run(v.initializer)
	return v

def shape(x):
	return x.get_shape()

def square(x):
	return tf.square(x)

def zeros(shape, dtype="float32", name=None):
	return variable(np.zeros(shape), dtype, name)

def concatenate(tensors, axis=-1):
	if axis < 0:
		axis = axis % len(tensors[0].get_shape())
	return tf.concat(axis, tensors)

def LRN2D(x):
	return tf.nn.lrn(x, alpha=1e-4, beta=0.75)

def conv2d_bn(x, layer=None, cv1_out=None, cv1_filter=(1,1), cv1_strides=(1,1),
				cv2_out=None, cv2_filter=(3,3), cv2_strides=(1,1), padding=None):
	num = '' if cv2_out == None else '1'
	tensor = Conv2D(cv1_out, cv1_filter, strides=cv1_strides, data_format="channels_first",
					name=layer+'_conv'+num)(x)
	tensor = BatchNormalization(axis=1, epsilon=0.00001, name=layer+"_bn"_num)(tensor)
	tensor = Activation("relu")(tensor)

	if padding == None:
		return tensor

	tensor = ZeroPadding2D(padding=padding, data_format="channels_first", name=layer+"_conv2")(tensor)
	tensor = BatchNormalization(axis=1, epsilon=0.00001, name=layer+"_bn2")(tensor)
	tensor = Activation("relu")(tensor)

	return tensor


WEIGHTS = [
  'conv1', 'bn1', 'conv2', 'bn2', 'conv3', 'bn3',
  'inception_3a_1x1_conv', 'inception_3a_1x1_bn',
  'inception_3a_pool_conv', 'inception_3a_pool_bn',
  'inception_3a_5x5_conv1', 'inception_3a_5x5_conv2', 'inception_3a_5x5_bn1', 'inception_3a_5x5_bn2',
  'inception_3a_3x3_conv1', 'inception_3a_3x3_conv2', 'inception_3a_3x3_bn1', 'inception_3a_3x3_bn2',
  'inception_3b_3x3_conv1', 'inception_3b_3x3_conv2', 'inception_3b_3x3_bn1', 'inception_3b_3x3_bn2',
  'inception_3b_5x5_conv1', 'inception_3b_5x5_conv2', 'inception_3b_5x5_bn1', 'inception_3b_5x5_bn2',
  'inception_3b_pool_conv', 'inception_3b_pool_bn',
  'inception_3b_1x1_conv', 'inception_3b_1x1_bn',
  'inception_3c_3x3_conv1', 'inception_3c_3x3_conv2', 'inception_3c_3x3_bn1', 'inception_3c_3x3_bn2',
  'inception_3c_5x5_conv1', 'inception_3c_5x5_conv2', 'inception_3c_5x5_bn1', 'inception_3c_5x5_bn2',
  'inception_4a_3x3_conv1', 'inception_4a_3x3_conv2', 'inception_4a_3x3_bn1', 'inception_4a_3x3_bn2',
  'inception_4a_5x5_conv1', 'inception_4a_5x5_conv2', 'inception_4a_5x5_bn1', 'inception_4a_5x5_bn2',
  'inception_4a_pool_conv', 'inception_4a_pool_bn',
  'inception_4a_1x1_conv', 'inception_4a_1x1_bn',
  'inception_4e_3x3_conv1', 'inception_4e_3x3_conv2', 'inception_4e_3x3_bn1', 'inception_4e_3x3_bn2',
  'inception_4e_5x5_conv1', 'inception_4e_5x5_conv2', 'inception_4e_5x5_bn1', 'inception_4e_5x5_bn2',
  'inception_5a_3x3_conv1', 'inception_5a_3x3_conv2', 'inception_5a_3x3_bn1', 'inception_5a_3x3_bn2',
  'inception_5a_pool_conv', 'inception_5a_pool_bn',
  'inception_5a_1x1_conv', 'inception_5a_1x1_bn',
  'inception_5b_3x3_conv1', 'inception_5b_3x3_conv2', 'inception_5b_3x3_bn1', 'inception_5b_3x3_bn2',
  'inception_5b_pool_conv', 'inception_5b_pool_bn',
  'inception_5b_1x1_conv', 'inception_5b_1x1_bn',
  'dense_layer'
]

conv_shape = {
  'conv1': [64, 3, 7, 7],
  'conv2': [64, 64, 1, 1],
  'conv3': [192, 64, 3, 3],
  'inception_3a_1x1_conv': [64, 192, 1, 1],
  'inception_3a_pool_conv': [32, 192, 1, 1],
  'inception_3a_5x5_conv1': [16, 192, 1, 1],
  'inception_3a_5x5_conv2': [32, 16, 5, 5],
  'inception_3a_3x3_conv1': [96, 192, 1, 1],
  'inception_3a_3x3_conv2': [128, 96, 3, 3],
  'inception_3b_3x3_conv1': [96, 256, 1, 1],
  'inception_3b_3x3_conv2': [128, 96, 3, 3],
  'inception_3b_5x5_conv1': [32, 256, 1, 1],
  'inception_3b_5x5_conv2': [64, 32, 5, 5],
  'inception_3b_pool_conv': [64, 256, 1, 1],
  'inception_3b_1x1_conv': [64, 256, 1, 1],
  'inception_3c_3x3_conv1': [128, 320, 1, 1],
  'inception_3c_3x3_conv2': [256, 128, 3, 3],
  'inception_3c_5x5_conv1': [32, 320, 1, 1],
  'inception_3c_5x5_conv2': [64, 32, 5, 5],
  'inception_4a_3x3_conv1': [96, 640, 1, 1],
  'inception_4a_3x3_conv2': [192, 96, 3, 3],
  'inception_4a_5x5_conv1': [32, 640, 1, 1,],
  'inception_4a_5x5_conv2': [64, 32, 5, 5],
  'inception_4a_pool_conv': [128, 640, 1, 1],
  'inception_4a_1x1_conv': [256, 640, 1, 1],
  'inception_4e_3x3_conv1': [160, 640, 1, 1],
  'inception_4e_3x3_conv2': [256, 160, 3, 3],
  'inception_4e_5x5_conv1': [64, 640, 1, 1],
  'inception_4e_5x5_conv2': [128, 64, 5, 5],
  'inception_5a_3x3_conv1': [96, 1024, 1, 1],
  'inception_5a_3x3_conv2': [384, 96, 3, 3],
  'inception_5a_pool_conv': [96, 1024, 1, 1],
  'inception_5a_1x1_conv': [256, 1024, 1, 1],
  'inception_5b_3x3_conv1': [96, 736, 1, 1],
  'inception_5b_3x3_conv2': [384, 96, 3, 3],
  'inception_5b_pool_conv': [96, 736, 1, 1],
  'inception_5b_1x1_conv': [256, 736, 1, 1],
}


def load_weights_from_FaceNet(FRmodel):
	weights = WEIGHTS
	weights_dict = load_weigths()

	for name in weights:
		if FRmodel.get_layer(name) != None:
			FRmodel.get_layer(name).set_weights(weights_dict[name])
		elif model.get_layer(name) != None:
			model.get_layer(name).set_weights(weights_dict[name])


def load_weights():
	path = "./weights"
	fileNames = filter(lambda f: not f.startswith('.'), os.listdir(path))
	paths = {}
	weights_dict = {}

	for n in fileNames:
		paths[n.replace(".csv", "")] = path + "/" + n

	for name in WEIGHTS:
		if 'conv' in name:
			conv_w = np.genfromtxt(paths[name + "_w"], delimiter=',', dtype=None)
			conv_w = np.reshape(conv_w, conv_shape[name])
			conv_w = np.transpose(conv_w, (2, 3, 1, 0))
			
			conv_b = np.genfromtxt(paths[name + "_b"], delimiter=",", dtype=None)
			weights_dict[name] = [conv_w, conv_b]
		elif "bn" in name:
			bn_w = np.genfromtxt(paths[name + "_w"], delimiter=',', dtype=None)
			bn_b = np.genfromtxt(paths[name + "_b"], delimiter=',', dtype=None)
			bn_m = np.genfromtxt(paths[name + "_m"], delimiter=',', dtype=None)
			bn_v = np.genfromtxt(paths[name + "_v"], delimiter=',', dtype=None)
			weights_dict[name] = [bn_w, bn_b, bn_m, bn_v]
		elif "dense" in name:
			dense_w = np.genfromtxt(paths[name + "_w"], delimiter=',', dtype=None)
			dense_w = np.reshape(dense_w, (128, 736))
			dense_w = np.transpose(dense_w, (1, 0))
			dense_b = np.genfromtxt(path + "/dense_b.csv", delimiter=",", dtype=None)
			weights_dict[name] = [dense_w, dense_b]

	return weights_dict


def load_dataset():
	train_dataset = h5py.File("datasets/train_happy.h5", "r")
	train_set_x = np.array(train_dataset["train_set_x"][:])
	train_set_y = np.array(train_dataset["train_set_y"][:])

	test_dataset = h5py.File("datasets/test_happy.h5", "r")
	test_set_x = np.array(train_dataset["test_set_x"][:])
	test_set_y = np.array(train_dataset["test_set_y"][:])

	classes = np.array(test_dataset["list_classes"][:])

	train_set_y = train_set_y.reshape((1, train_set_y.shape[0]))
	test_set_y = test_set_y.reshape((1, test_set_y.shape[0]))

	return train_set_x, train_set_y, test_set_x, test_set_y, classes


def img_to_enoding(img_path, model):
	img1 = cv2.imread(img_path, 1)
	img = img1[...,::-1]
	img = np.around(np.transpose(img, (2, 0, 1))/255.0, decimals=12)
	x_train = np.array([img])
	embedding = model.predict_on_batch(x_train)

	return embedding
