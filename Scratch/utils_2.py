import matplotlib.pyplot as plt
import numpy as np

# -----------------------------------------------
# ---------------   ACTIVATIONS   ---------------
# -----------------------------------------------

def sigmoid(z):
    A =  1 / (1 + np.exp(-z))
    cache = z
    return A, cache


def sigmoid_backward(dA, cache):
    z = cache

    s = 1 / ( 1 + np.exp(-z))
    dZ = s * dA * (1 - s)
    return dZ


def relu(z):
    A = np.maximum(0, z)
    cache = z
    return A, cache


def relu_backward(dA, cache):
    Z = cache
    dZ = np.array(dA, copy=True)
    dZ[Z <= 0] = 0

    return dZ


# ----------------------------------------------
# ---------------   PARAMETERS   ---------------
# ----------------------------------------------


def init_params(n_x, n_h, n_y):
    W1 = np.random.randn(n_h, n_x) * 0.01
    b1 = np.zeros((n_h, 1))
    W2 = np.random.randn(n_y, n_h) * 0.01
    b2 = np.zeros((n_y, 1))

    params = {
        "W1":W1,
        "b1":b1,
        "W2":W2,
        "b2":b2
    }

    return params


def update_params(params, grads, learning_rate):
    L = len(params) // 2 # number of layers in neural network

    for l in range(L):
        params["W"+str(l+1)] = params["W"+str(l+1)] - learning_rate * grads["dW"+str(l+1)]
        params["b"+str(l+1)] = params["b"+str(l+1)] - learning_rate * grads["db"+str(l+1)]
        
    return params


# ---------------------------------------------
# -------------   COST FUNCTION   -------------
# ---------------------------------------------

def compute_cost(AL, Y):
    m = Y.shape[1]

    cost = (-1/m) * (np.dot(Y, np.log(AL).T) + np.dot(1 - Y, np.log(1 - AL).T))
    
    return np.squeeze(cost)


# ------------------------------------------------
# -------------   LINEAR FUNCTIONS   -------------
# ------------------------------------------------

def linear_forward(A, W, b):
    # A - activation from previous layer (or input data)
    # (size of previous layer, number of examples)
    Z = W.dot(A) + b
    cache = (A, W, b)
    return Z, cache


def linear_activation_forward(A_prev, W, b, activation="relu"):

    if activation == "relu":
        Z, linear_cache = linear_forward(A_prev, W, b)
        A, activation_cache = relu(Z)
    elif activation == "sigmoid":
        Z, linear_cache = linear_forward(A_prev, W, b)
        A, activation_cache = sigmoid(Z)

    cache = (linear_cache, activation_cache)

    return A, cache


def linear_backward(dZ, cache):
    A_prev, W, b = cache
    m = A_prev.shape[1]

    dW = (1/m)*np.dot(dZ, A_prev.T)
    db = (1/m)*np.sum(dZ, axis=1, keepdims=True)

    dA_prev = np.dot(W.T, dZ)

    return dA_prev, dW, db


def linear_activation_backward(dA, cache, activation):
    linear_cache, activation_cache = cache

    if activation == "relu":
        dZ = relu_backward(dA, activation_cache)
    elif activation == "sigmoid":
        dZ = sigmoid_backward(dA, activation_cache)

    dA_prev, dW, db = linear_backward(dZ, linear_cache)

    return dA_prev, dW, db


# -----------------------------------------------
# ---------------   PREDICTIONS   ---------------
# -----------------------------------------------

from utils_Lmodel import L_model_forward

def predict(X, Y, params):
    m = X.shape[1]
    n = len(params)//2 #num of layers in neural network
    p = np.zeros((1, m))

    probs, caches = L_model_forward(X, params)

    for i in range(probs.shape[1]):
        if probs[0, i] > 0.5:
            p[0, 1] = 1
        else:
            p[0, i] = 0

    print("Accuracy: {}".format(np.sum((p==Y)/m)))

    return p
