import cv2, os

def flip_images(update_id):
	gest_folder = "gestures"
	count = 0
	total = len(os.listdir(gest_folder))
	images_labels = []
	images = []
	labels = []
	for g_id in os.listdir(gest_folder):
		for i in range(1200):
			path = gest_folder+"/"+g_id+"/"+str(i+1)+".jpg"
			new_path = gest_folder+"/"+g_id+"/"+str(i+1+1200)+".jpg"
			print(path)
			img = cv2.imread(path, 0)
			img = cv2.flip(img, 1)
			cv2.imwrite(new_path, img)

			count += 1
			flip_images_progressbar = count / (1200 * total) * 100
			update_id(flip_images_progressbar)


#REDACTED
#flip_images()
