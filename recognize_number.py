import cv2, pickle
import numpy as np
import tensorflow as tf
from cnn_tf import cnn_model_fn
import os
import sqlite3
from keras.models import load_model
from PIL import ImageFont, ImageDraw, Image

#edit import import absl-py package


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

#edit
#tf.logging.set_verbosity(tf.logging.ERROR)
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
classifier = tf.estimator.Estimator(model_dir="tmp/cnn_model2", model_fn=cnn_model_fn)
prediction = None
model = load_model('cnn_model_keras2_number.h5')

def get_image_size():
	img = cv2.imread('gestures/0/100.jpg', 0)
	return img.shape

image_x, image_y = get_image_size()

def tf_process_image(img):
	img = cv2.resize(img, (image_x, image_y))
	img = np.array(img, dtype=np.float32)
	np_array = np.array(img)
	return np_array

def tf_predict(classifier, image):
	'''
	need help with prediction using tensorflow
	'''
	global prediction
	processed_array = tf_process_image(image)
	#edit pred_input_fn = tf.estimator.inputs.numpy_input_fn(x={"x":processed_array}, shuffle=False)
	pred_input_fn = tf.compat.v1.estimator.inputs.numpy_input_fn(x={"x":processed_array}, shuffle=False)
	pred = classifier.predict(input_fn=pred_input_fn)
	prediction = next(pred)
	print(prediction)

def keras_process_image(img):
	img = cv2.resize(img, (image_x, image_y))
	img = np.array(img, dtype=np.float32)
	img = np.reshape(img, (1, image_x, image_y, 1))
	return img

def keras_predict(model, image):
	processed = keras_process_image(image)
	pred_probab = model.predict(processed)[0]
	pred_class = list(pred_probab).index(max(pred_probab))
	return max(pred_probab), pred_class

def get_pred_text_from_db(pred_class):
	conn = sqlite3.connect("gesture_db2.db")
	cmd = "SELECT g_name FROM gesture WHERE g_id="+str(pred_class)
	cursor = conn.execute(cmd)
	for row in cursor:
		return row[0]



def get_language_dictionary(text):
	try:
		conn = sqlite3.connect("gesture_db2.db")
		cmd = "SELECT * FROM language WHERE l_name=" + str(text)
		cursor = conn.execute(cmd)
		for row in cursor:
			#text2 = text + "  English: "+ row[2] + "  \nMalay: "+ row[3] + "\nChinese: "+ row[4] +"\nTamil: "+ row[5]
			#return (text2)
			return row
	except sqlite3.Error:
		return str(text)



def put_splitted_text_in_blackboard(blackboard, splitted_text):
	y = 200

	for text in splitted_text:
		cv2.putText(blackboard, text, (4, y), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 255, 255))
		y += 50

def get_hand_hist():
	with open("hist", "rb") as f:
		hist = pickle.load(f)
	return hist

def recognize():
	global prediction
	flagPressedP = True
	cam = cv2.VideoCapture(1)
	if cam.read()[0] == False:
		cam = cv2.VideoCapture(0)
	hist = get_hand_hist()
	x, y, w, h = 300, 100, 300, 300
	while True:
		text = ""
		img = cam.read()[1]
		img = cv2.flip(img, 1)
		img = cv2.resize(img, (640, 480))
		#imgCrop = img[y:y+h, x:x+w]
		#imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		#dst = cv2.calcBackProject([imgHSV], [0, 1], hist, [0, 180, 0, 256], 1)
		disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(10,10))
		grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		dst = grayImage
		#cv2.filter2D(dst,-1,disc,dst)
		blur = cv2.GaussianBlur(dst, (11,11), 0)
		blur = cv2.medianBlur(blur, 15)
		if flagPressedP:
			# SKIN ISSUE
			# if black skin white background:
			thresh = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
		else:
			# If white skin black background:
			thresh = cv2.threshold(blur,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]

		thresh = cv2.merge((thresh,thresh,thresh))
		thresh = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
		thresh = thresh[y:y+h, x:x+w]
		(openCV_ver,_,__) = cv2.__version__.split(".")
		if openCV_ver=='3':
			contours = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[1]
		elif openCV_ver=='4':
			contours = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]
		if len(contours) > 0:
			contour = max(contours, key = cv2.contourArea)
			#print(cv2.contourArea(contour))
			if cv2.contourArea(contour) > 10000:
				x1, y1, w1, h1 = cv2.boundingRect(contour)
				save_img = thresh[y1:y1+h1, x1:x1+w1]
				
				if w1 > h1:
					save_img = cv2.copyMakeBorder(save_img, int((w1-h1)/2) , int((w1-h1)/2) , 0, 0, cv2.BORDER_CONSTANT, (0, 0, 0))
				elif h1 > w1:
					save_img = cv2.copyMakeBorder(save_img, 0, 0, int((h1-w1)/2) , int((h1-w1)/2) , cv2.BORDER_CONSTANT, (0, 0, 0))
				
				pred_probab, pred_class = keras_predict(model, save_img)
				#edit #replace pred_probab, pred_class = tf_predict(classifier, save_img)
				print(pred_probab)

				if pred_probab*100 > 80:
					text = get_pred_text_from_db(pred_class)
					#text = '1'
					#print(text)
		#edit variable either a string or an array
		text = get_language_dictionary(text)
		#print(pred_class)
		blackboard = np.zeros((480, 640, 3), dtype=np.uint8)

		if isinstance(text, tuple):
			#name and english and Malay
			cv2.putText(blackboard, text[1], (30, 120), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 255, 255))
			cv2.putText(blackboard, "English: "+text[2], (30, 180), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (255, 255, 255))
			cv2.putText(blackboard, "Melayu: "+text[3], (30, 240), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (255, 255, 255))

			## Use simsum.ttc to write Chinese & Tamil_MN to write Tamil.
			fontpath = "./font/simsun.ttc"  # <== ?????????????????????
			font = ImageFont.truetype(fontpath, 50)
			img_pil = Image.fromarray(blackboard)
			draw = ImageDraw.Draw(img_pil)
			draw.text((30, 270), "????????? "+text[4], font=font, fill=(255, 255, 255, 0))
			blackboard = np.array(img_pil)

			## Use Uni-Tamil195.ttc to write Chinese.
			fontpath2 = "./font/Tamil_MN.ttc"  # <== internet download
			font2 = ImageFont.truetype(fontpath2, 50)
			img_pil2 = Image.fromarray(blackboard)
			draw2 = ImageDraw.Draw(img_pil2)
			draw2.text((30, 340), "???????????????: "+text[5], font=font2, fill=(255, 255, 255, 0))
			blackboard = np.array(img_pil2)

		else:
			# alphabet
			print(text)
			cv2.putText(blackboard, text, (30, 200), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 255, 255))

		cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
		res = np.hstack((img, blackboard))
		cv2.imshow("Recognizing gesture", res)
		cv2.imshow("thresh", thresh)
		if cv2.waitKey(1) == ord('q'):
			cam.release()
			cv2.destroyAllWindows()
			break
		elif cv2.waitKey(1) == ord('p'):
			if flagPressedP:
				flagPressedP = False
			else:
				flagPressedP = True

def run_recognize_number():
	keras_predict(model, np.zeros((50, 50), dtype=np.uint8))
	#edit #replace tf_predict(classifier, np.zeros((50, 50), dtype=np.uint8))
	recognize()

# needed .h5 , gesture_db2.db