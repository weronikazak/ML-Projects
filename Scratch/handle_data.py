import numpy as np
import h5py

def load_data(data_name):
	if data_name == "signs":
		train_file = "data/train_signs.h5"
		test_file = "data/test_signs.h5"
	elif data_name == "happy":
		train_file = "data/train_happy.h5"
		test_file = "data/test_happy.h5"

	train_dataset = h5py.File(train_file, "r")
	X_train = np.array(train_dataset["train_set_x"][:])
	Y_train = np.array(train_dataset["train_set_y"][:])

	test_dataset = h5py.File(test_file, "r")
	X_test = np.array(test_dataset["test_set_x"][:])
	Y_test = np.array(test_dataset["test_set_y"][:])

	classes = np.array(test_dataset["list_classes"][:])

	Y_train = Y_train.reshape((1, Y_train.shape[0]))
	Y_test = Y_test.reshape((1, Y_test.shape[0]))

	return X_train, Y_train, X_test, Y_test, classes