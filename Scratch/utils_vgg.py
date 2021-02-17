import matplotlib.pyplot as plt
import numpy as np
import sklearn
import tensorflow.compat.v1 as tf
import scipy
import scipy.io
import scipy.misc
import PIL
from PIL import Image
import os
import sys


def load_vgg_model(path):
	vgg = scipy.io.loadmat(path)

	vgg_layers = vgg["layers"]

	def _weights(layer, expected_layer_name):
		c = vgg_layers[0][layer]
		W = vgg_layers[0][layer][0][0][0][0][0]
		# print(W)
		b = vgg_layers[0][layer][0][0][0][0][1]

		layer_name = vgg_layers[0][layer][0][0][0]

		return W, b


	def _relu(conv2d_layer):
		return tf.nn.relu(conv2d_layer)


	def _conv2d(prev_layer, layer, layer_name):
		W, b = _weights(layer, layer_name)
		W = tf.constant(W)
		b = tf.constant(np.reshape(b, (b.size)))

		return tf.nn.conv2d(prev_layer, filters=W, strides=[1, 1, 1, 1], padding="SAME") + b


	def _conv2d_relu(prev_layer, layer, layer_name):
		return _relu(_conv2d(prev_layer, layer, layer_name))


	def _avgpool(prev_layer):
		return tf.nn.avg_pool(prev_layer, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="SAME")


	graph = {}
	graph["input"]    =  tf.Variable(np.zeros((1, 450, 600, 3)), dtype='float32')
	graph['conv1_1']  =  _conv2d_relu(graph['input'], 0, 'conv1_1')
	graph["conv1_2"]  =  _conv2d_relu(graph['conv1_1'], 2, 'conv1_2')
	graph["avgpool1"] =  _avgpool(graph['conv1_2'])

	graph["conv2_1"]  =  _conv2d_relu(graph["avgpool1"], 5, "conv2_1")
	graph["conv2_2"]  =  _conv2d_relu(graph["conv2_1"], 7, "conv2_2")
	graph["avgpool2"] =  _avgpool(graph['conv2_2'])

	graph["conv3_1"]  =  _conv2d_relu(graph["avgpool2"], 10, "conv3_1")
	graph["conv3_2"]  =  _conv2d_relu(graph["conv3_1"], 12, "conv3_2")
	graph["conv3_3"]  =  _conv2d_relu(graph["conv3_2"], 14, "conv3_3")
	graph["conv3_4"]  =  _conv2d_relu(graph["conv3_3"], 16, "conv3_4")
	graph["avgpool3"] =  _avgpool(graph['conv3_4'])

	graph["conv4_1"]  =  _conv2d_relu(graph["avgpool3"], 19, "conv4_1")
	graph["conv4_2"]  =  _conv2d_relu(graph["conv4_1"], 21, "conv4_2")
	graph["conv4_3"]  =  _conv2d_relu(graph["conv4_2"], 23, "conv4_3")
	graph["conv4_4"]  =  _conv2d_relu(graph["conv4_3"], 25, "conv4_4")
	graph["avgpool4"] =  _avgpool(graph['conv4_4'])

	graph["conv5_1"]  =  _conv2d_relu(graph["avgpool4"], 28, "conv5_1")
	graph["conv5_2"]  =  _conv2d_relu(graph["conv5_1"], 30, "conv5_2")
	graph["conv5_3"]  =  _conv2d_relu(graph["conv5_2"], 32, "conv5_3")
	graph["conv5_4"]  =  _conv2d_relu(graph["conv5_3"], 34, "conv5_4")
	graph["avgpool5"] =  _avgpool(graph['conv5_4'])

	return graph


def generate_noise_img(content_img, noise_ratio=0.6):
	noise_img = np.random.uniform(-20, 20, (1, 450, 600, 3)).astype("float32") 

	input_img = noise_img * noise_ratio + content_img * (1 - noise_ratio)

	return input_img


def reshape_and_normalize_img(img):
	img = np.reshape(img, ((1, ) + img.shape))
	means = np.array([123.68, 116.779, 103.939]).reshape((1,1,1,3)) 
	img = img - means

	return img


def resize_img(img_path):
	img = Image.open(img_path)
	baseheight = 450 
	hpercent = (baseheight / float(img.size[1]))
	wsize = int((float(img.size[0]) * float(hpercent)))
	img = img.resize((wsize, baseheight), PIL.Image.ANTALIAS)

	img = img.crop((0, 0, 600, 450))

	img_array = np.array(img.getdata(), np.uint8).reshape(img.size[1]. img.size[0], 3)

	return img_array

def get_imgs():
	content_img_path = "images/catto.jpg"
	content_img = resize_img(content_img_path)
	content_img = reshape_and_normalize_img(content_img)

	style_img_path = "images/scream.jpg"
	style_img = resize_img(style_img_path)
	style_img = reshape_and_normalize_img(style_img)

	generated_img = generate_noise_img(content_img)

	return (content_img, style_img, generated_img)

def save_img(path, img):
	means = np.array([123.68, 116.779, 103.939]).reshape((1,1,1,3)) 
	img = img + means

	img = np.clip(img[0], 0, 255).astype("uint8")
	scipy.misc.imsave(path, img)
