import numpy as np
from utils_2 import *

def init_params_L(layer_dims):
	params = {}
	L = len(layer_dims)

	for l in range(1, L):
		params["W"+str(l)] = np.random.randn(layer_dims[l], layer_dims[l-1]) / np.sqrt(layer_dims[l-1])
		params["b"+str(l)] = np.zeros((layer_dims[l], 1))

	return params


def L_model_forward(X, params):
	caches = []
	A = X
	L = len(params) // 2

	for i in range(1, L):
		A_prev = A
		A, cache = linear_activation_forward(A_prev, params["W"+str(i)], params["b"+(str(i))], activation="relu")
		caches.append(cache)

	AL, cache = linear_activation_forward(A, params["W"+str(L)], params["b"+(str(L))], activation="sigmoid")
	caches.append(cache)

	return AL, caches


def L_model_backward(AL, Y, caches):
	grads = {}
	L = len(caches)
	Y = Y.reshape(AL.shape)

	dAL = -(np.divide(Y, AL) - np.divide(1 - Y, 1 - AL))

	current_cache = caches[L-1]
	grads["dA"+str(L-1)], grads["dW"+str(L)], grads["db"+str(L)] = linear_activation_backward(dAL, current_cache, activation="sigmoid")

	for l in reversed(range(L-1)):
		current_cache = caches[l]
		dA_prev_t, dW_t, db_t = linear_activation_backward(grads["dA"+str(l+1)], current_cache, activation="relu")
		grads["dA"+str(l)] = dA_prev_t
		grads["dW"+str(l+1)] = dW_t
		grads["db"+str(l+1)] = db_t

	return grads