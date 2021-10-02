import matplotlib.pyplot as plt
import numpy as np

# -----------------------------------------------
# ---------------   ACTIVATIONS   ---------------
# -----------------------------------------------

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def relu(z):
    return np.maximum(0, z)


# ----------------------------------------------
# ---------------   PARAMETERS   ---------------
# ----------------------------------------------


def init_params(layers_dims):
    params = {}
    L = len(layers_dims)
    for l in range(1, L):
        params["W"+str(l)] = np.random.randn(layers_dims[l], layers_dims[l-1])/ np.sqrt(layers_dims[l-1])
        params["b"+str(l)] = np.zeros((layers_dims[l], 1))
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

def compute_cost(A3, Y):
    m = Y.shape[1]
    
    logprobs = np.multiply(-np.log(A3),Y) + np.multiply(-np.log(1 - A3), 1 - Y)
    cost = 1./m * np.nansum(logprobs)
    
    return cost


# -----------------------------------------------
# ---------------   PROPAGATIONS  ---------------
# -----------------------------------------------

def forward_propagation(X, params):
    W1 = params["W1"]
    b1 = params["b1"]
    W2 = params["W2"]
    b2 = params["b2"]
    W3 = params["W3"]
    b3 = params["b3"]
    
    Z1 = np.dot(W1, X) + b1
    A1 = relu(Z1)
    Z2 = np.dot(W2, A1) + b2
    A2 = relu(Z2)
    Z3 = np.dot(W3, A2) + b3
    A3 = sigmoid(Z3)
    
    cache = (Z1, A1, W1, b1, Z2, A2, W2, b2, Z3, A3, W3, b3)
    
    return A3, cache

def backprop(X, Y, cache):
    m = X.shape[1]
    (Z1, A1, W1, b1, Z2, A2, W2, b2, Z3, A3, W3, b3) = cache
    
    dZ3 = 1./m * (A3 - Y) # backprop sigmoid
    dW3 = np.dot(dZ3, A2.T)
    db3 = np.sum(dZ3, axis=1, keepdims=True)
    
    dA2 = np.dot(W3.T, dZ3)
    dZ2 = np.multiply(dA2, np.int64(A2 > 0)) # backprop relu
    dW2 = np.dot(dZ2, A1.T)
    db2 = np.sum(dZ2, axis=1, keepdims=True)
    
    dA1 = np.dot(W2.T, dZ2)
    dZ1 = np.multiply(dA1, np.int64(A1 > 0))
    dW1 = np.dot(dZ1, X.T)
    db1 = np.sum(dZ1, axis=1, keepdims=True)
    
    grads = {
        "dZ3":dZ3, "dW3":dW3, "db3":db3,
        "dZ2":dZ2, "dA2":dA2, "dW2":dW2, "db2":db2,
        "dZ1":dZ1, "dA1":dA1, "dW1":dW1, "db1":db1
    }
    
    return grads

# ----------------------------------------------
# ---------------   PREDICTIONS  ---------------
# ----------------------------------------------

def predict(X, Y, params):
    m = X.shape[1]
    p = np.zeros((1,m), dtype = np.int)
    
    A3, caches = forward_propagation(X, params)
    
    for i in range(0, A3.shape[1]):
        if A3[0,i] > 0.5:
            p[0,i] = 1
        else:
            p[0,i] = 0

    print("Accuracy: "  + str(np.mean((p[0,:] == Y[0,:]))))
    
    return p

def predict_dec(params, X):
    A3, cache = forward_propagation(X, params)
    preds = (A3 > 0.5)
    return preds