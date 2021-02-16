import matplotlib.pyplot as plt
import numpy as np
import sklearn
import sklearn.datasets
import sklearn.linear_model

def load_vgg_model(path):
	vgg = scipy.io.loadmat(path)

	vgg_layers = vgg["layers"]

	def _weights(layer, expected_layer_name):
		wb = vgg_layers[0][layer][0][0][2]
		W = wb[0][0]
		b = wb[0][1]
		layer_name = vgg_layers[0][layer][0][0][0][0]

		assert layer_name == expected_layer_name
		return W, b


	def _relu(conv2d_layer):
		return tf.nn.relu(conv2d_layer)


	def _conv2d(prev_layer, layer, layer_name):
		W, b = _weights(layer, layer_name)
		W = tf.constant(W)
		b = tf.constant(np.reshape(b, (b.size)))

		return tf.nn.conv2d(prev_layer, filter=W, strides=[1, 1, 1, 1], padding="SAME") + b


	def _conv2d_relu(prev_layer, layer, layer_name):
		return _relu(_conv2d(prev_layer, layer, layer_name))


	def _avgpool(prev_layer):
		return tf.nn.avg_pool(prev_layer, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], apdding="SAME")


	graph = {}
	graph["input"] = tf.Variable(np.zeros((1, CONFIG.IMAGE_HEIGHT, CONFIG.IMAGE_WIDTH, CONFIG.COLOR_CHANNELS)), dtype='float32')
	graph["conv1_1"] = _conv2d_relu(graph['input'], 0, 'conv1_1')
	graph["conv1_2"] = _conv2d_relu(graph['conv1_1'], 2, 'conv1_2')
	graph["avgpool1"] = _avgpool(graph['conv1_2'])

	graph["conv2_1"] = _conv2d_relu(graph["avgpool1"], 5, "conv2_1")
	graph["conv2_2"] = _conv2d_relu(graph["conv2_1"], 7, "conv2_2")
	graph["avgpool2"] = _avgpool(graph['conv2_2'])

	graph["conv3_1"] = _conv2d_relu(graph["avgpool2"], 10, "conv3_1")
	graph["conv3_2"] = _conv2d_relu(graph["conv3_1"], 12, "conv3_2")
	graph["conv3_3"] = _conv2d_relu(graph["conv3_2"], 14, "conv3_3")
	graph["conv3_4"] = _conv2d_relu(graph["conv3_3"], 16, "conv3_4")
	graph["avgpool3"] = _avgpool(graph['conv3_4'])

	graph["conv4_1"] = _conv2d_relu(graph["avgpool3"], 10, "conv4_1")
	graph["conv4_2"] = _conv2d_relu(graph["conv4_1"], 12, "conv4_2")
	graph["conv4_3"] = _conv2d_relu(graph["conv4_2"], 14, "conv4_3")
	graph["conv4_4"] = _conv2d_relu(graph["conv4_3"], 16, "conv4_4")
	graph["avgpool4"] = _avgpool(graph['conv4_4'])

	graph["conv5_1"] = _conv2d_relu(graph["avgpool4"], 10, "conv5_1")
	graph["conv5_2"] = _conv2d_relu(graph["conv5_1"], 12, "conv5_2")
	graph["conv5_3"] = _conv2d_relu(graph["conv5_2"], 14, "conv5_3")
	graph["conv5_4"] = _conv2d_relu(graph["conv5_3"], 16, "conv5_4")
	graph["avgpool5"] = _avgpool(graph['conv5_4'])

	return graph


def generate_noise_img(content_img, noise_ratio=0.6):
	noise_img = np.random.uniform(-20, 20, (1, 600, 600, 3).astype("float32")) 

	input_img = noise_img * noise_ratio + content_img * (1 - noise_ratio)

	return input_img


def reshape_and_normalize_img(img):
	img = np.reshape(img, ((1, ) + img.shape))
	means = np.array([123.68, 116.779, 103.939]).reshape((1,1,1,3)) 
	img = img - means

	return img

