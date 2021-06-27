import tensorflow as tf
import numpy as np
import pickle, os, cv2



#edit
#tf.logging.set_verbosity(tf.logging.INFO)
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.INFO)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

def get_image_size():
	img = cv2.imread('gestures/0/100.jpg', 0)

	return img.shape

def get_num_of_classes():
	return len(os.listdir('gestures/'))

image_x, image_y = get_image_size()

def cnn_model_fn(features, labels, mode):
	input_layer = tf.reshape(features["x"], [-1, image_x, image_y, 1], name="input")

	#edit conv1 = tf.layers.conv2d(
	conv1 = tf.compat.v1.layers.conv2d(
	  inputs=input_layer,
	  filters=16,
	  kernel_size=[2, 2],
	  padding="same",
	  activation=tf.nn.relu,
	  name="conv1")
	print("conv1",conv1.shape)
	#edit pool1 = tf.layers.max_pooling2d(inputs=conv1, pool_size=[2, 2], strides=2, name="pool1")
	pool1 = tf.compat.v1.layers.max_pooling2d(inputs=conv1, pool_size=[2, 2], strides=2, name="pool1")
	print("pool1",pool1.shape)

	#edit conv2 = tf.layers.conv2d(
	conv2 = tf.compat.v1.layers.conv2d(
	  inputs=pool1,
	  filters=32,
	  kernel_size=[5, 5],
	  padding="same",
	  activation=tf.nn.relu,
	  name="conv2")
	print("conv2",conv2.shape)
	#edit pool2 = tf.layers.max_pooling2d(inputs=conv2, pool_size=[5, 5], strides=5, name="pool2")
	pool2 = tf.compat.v1.layers.max_pooling2d(inputs=conv2, pool_size=[5, 5], strides=5, name="pool2")
	print("pool2",pool2.shape)

	#edit conv3 = tf.layers.conv2d(
	conv3 = tf.compat.v1.layers.conv2d(
	  inputs=pool2,
	  filters=64,
	  kernel_size=[5, 5],
	  padding="same",
	  activation=tf.nn.relu,
	  name="conv3")
	print("conv3",conv3.shape)

	# Dense Layer
	flat = tf.reshape(conv3, [-1, 5*5*64], name="flat")
	print(flat.shape)
	#edit dense = tf.layers.dense(inputs=flat, units=128, activation=tf.nn.relu, name="dense")
	dense = tf.compat.v1.layers.dense(inputs=flat, units=128, activation=tf.nn.relu, name="dense")
	print(dense.shape)
	#edit dropout = tf.layers.dropout(inputs=dense, rate=0.2, training=mode == tf.estimator.ModeKeys.TRAIN, name="dropout")
	dropout = tf.compat.v1.layers.dropout(inputs=dense, rate=0.2, training=mode == tf.estimator.ModeKeys.TRAIN, name="dropout")

	# Logits Layer
	num_of_classes = get_num_of_classes()
	#edit logits = tf.layers.dense(inputs=dropout, units=num_of_classes, name="logits")
	logits = tf.compat.v1.layers.dense(inputs=dropout, units=num_of_classes, name="logits")

	output_class = tf.argmax(input=logits, axis=1, name="output_class")
	output_probab = tf.nn.softmax(logits, name="softmax_tensor")
	predictions = {"classes": tf.argmax(input=logits, axis=1), "probabilities": tf.nn.softmax(logits, name="softmax_tensor")}
	#tf.Print(tf.nn.softmax(logits, name="softmax_tensor"), [tf.nn.softmax(logits, name="softmax_tensor")])
	if mode == tf.estimator.ModeKeys.PREDICT:
		return tf.estimator.EstimatorSpec(mode=mode, predictions=predictions)

	# Calculate Loss (for both TRAIN and EVAL modes)
	onehot_labels = tf.one_hot(indices=tf.cast(labels, tf.int32), depth=num_of_classes)
	#edit loss = tf.losses.softmax_cross_entropy(onehot_labels=onehot_labels, logits=logits)
	loss = tf.compat.v1.losses.softmax_cross_entropy(onehot_labels=onehot_labels, logits=logits)

	# Configure the Training Op (for TRAIN mode)
	if mode == tf.estimator.ModeKeys.TRAIN:
		#edit optimizer = tf.train.GradientDescentOptimizer(learning_rate=1e-2)
		optimizer = tf.compat.v1.train.GradientDescentOptimizer(learning_rate=1e-2)
		#edit train_op = optimizer.minimize(loss=loss, global_step=tf.train.get_global_step())
		train_op = optimizer.minimize(loss=loss, global_step=tf.compat.v1.train.get_global_step())
		return tf.estimator.EstimatorSpec(mode=mode, loss=loss, train_op=train_op)

	# Add evaluation metrics (for EVAL mode)
	#edit eval_metric_ops = {"accuracy": tf.metrics.accuracy(labels=labels, predictions=predictions["classes"])}
	eval_metric_ops = {"accuracy": tf.compat.v1.metrics.accuracy(labels=labels, predictions=predictions["classes"])}
	return tf.estimator.EstimatorSpec(mode=mode, loss=loss, eval_metric_ops=eval_metric_ops)

def main(argv):
	with open("train_images", "rb") as f:
		#edit train_images = np.array(pickle.load(f))
		train_images = np.array(pickle.load(f), dtype=np.float32)
	with open("train_labels", "rb") as f:
		train_labels = np.array(pickle.load(f), dtype=np.int32)

	with open("test_images", "rb") as f:
		#edit test_images = np.array(pickle.load(f))
		test_images = np.array(pickle.load(f), dtype=np.float32)
	with open("test_labels", "rb") as f:
		test_labels = np.array(pickle.load(f), dtype=np.int32)
	#print(len(train_images[1]), len(train_labels))

	classifier = tf.estimator.Estimator(model_fn=cnn_model_fn, model_dir="tmp/cnn_model3")

	tensors_to_log = {"probabilities": "softmax_tensor"}
	#edit logging_hook = tf.train.LoggingTensorHook(tensors=tensors_to_log, every_n_iter=50)
	logging_hook = tf.compat.v1.train.LoggingTensorHook(tensors=tensors_to_log, every_n_iter=50)

	#edit train_input_fn = tf.estimator.inputs.numpy_input_fn(x={"x": train_images}, y=train_labels, batch_size=500, num_epochs=10, shuffle=True)
	train_input_fn = tf.compat.v1.estimator.inputs.numpy_input_fn(x={"x": train_images}, y=train_labels, batch_size=500, num_epochs=10, shuffle=True)
	classifier.train(input_fn=train_input_fn, hooks=[logging_hook])

	# Evaluate the model and print results
	#edit eval_input_fn = tf.estimator.inputs.numpy_input_fn(
	eval_input_fn = tf.compat.v1.estimator.inputs.numpy_input_fn(
	  x={"x": test_images},
	  y=test_labels,
	  num_epochs=1,
	  shuffle=False)
	test_results = classifier.evaluate(input_fn=eval_input_fn)
	print(test_results)


if __name__ == "__main__":
	#edit tf.app.run()
	tf.compat.v1.app.run()