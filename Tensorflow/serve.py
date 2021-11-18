import tensorflow.compat.v1 as tf
import os

SAVE_PATH = "./save"
MODEL_NAME = "test"
VERSION = 1
SERVE_PATH = f"./serve/{MODEL_NAME}/{VERSION}"

checkpoint = tf.train.latest_checkpoint(SAVE_PATH)

tf.reset_default_graph()

with tf.Session() as sess:
	# import the saved graph
	saver = tf.train.import_meta_graph(checkpoint + ".meta")

	# get the graph for this session
	sess.run(tf.global_variables_initializer())

	# get the tensors that we need
	inputs = graph.get_tensor_by_name("inputs:0")
	predictions = graph.get_tensor_by_name("prediction/Sigmoid:0")

# create tensors info
model_input = tf.saved_model.utils.build_tensor_info(inputs)
model_output = tf.saved_model.utils.build_tensor_info(predictions)

# build signature definition
signature_definition = tf.saved_model.signature_def_utils.build_signature_def(
	inputs={"inputs":model_input},
	outputs={"outputs":model_output},
	method_name=
	tf.saved_model.signature_constants.PREDICT_METHOD_NAME)