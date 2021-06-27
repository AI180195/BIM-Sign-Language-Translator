import cv2
import numpy as np
import pickle, os, sqlite3, random

#edit
#setx OPENCV_VIDEOIO_PRIORITY_MSMF 0


def init_create_folder_database():
	# create the folder and database if not exist
	if not os.path.exists("gestures"):
		os.mkdir("gestures")
	if not os.path.exists("gesture_db.db"):
		conn = sqlite3.connect("gesture_db.db")
		create_table_cmd = "CREATE TABLE gesture ( g_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, g_name TEXT NOT NULL )"
		conn.execute(create_table_cmd)
		conn.commit()
		#create language table
		create_table_cmd2 = "CREATE TABLE language ( l_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, l_name TEXT NOT NULL , l_English TEXT NOT NULL, l_Malay TEXT NOT NULL, l_Chinese TEXT NOT NULL, l_Tamil TEXT NOT NULL)"
		conn.execute(create_table_cmd2)
		conn.commit()

def create_folder(folder_name):
	if not os.path.exists(folder_name):
		os.mkdir(folder_name)

def store_in_db(l_id, l_name, l_English, l_Malay, l_Chinese, l_Tamil):
	conn = sqlite3.connect("gesture_db.db")
	cmd = "INSERT INTO language (l_id, l_name, l_English, l_Malay, l_Chinese, l_Tamil) VALUES (%s, \'%s\', \'%s\', \'%s\', \'%s\', \'%s\')" % (l_id, l_name, l_English, l_Malay, l_Chinese, l_Tamil)
	try:
		conn.execute(cmd)
	except sqlite3.IntegrityError:
		choice = input("l_id already exists. Want to change the record? (y/n): ")
		if choice.lower() == 'y':
			cmd = "UPDATE language SET l_name = \'%s\', l_English = \'%s\', l_Malay = \'%s\', l_Chinese = \'%s\', l_Tamil = \'%s\' WHERE l_id = %s" % (l_name, l_English, l_Malay, l_Chinese, l_Tamil, l_id)
			conn.execute(cmd)
		else:
			print("Doing nothing...")
			return
	conn.commit()


init_create_folder_database()
l_id = input("Enter language no.: ")
l_name = input("Enter language name/text: ")
l_English = input("Enter language English: ")
l_Malay = input("Enter language Malay: ")
l_Chinese = input("Enter language Chinese: ")
l_Tamil = input("Enter language Tamil: ")
# print(l_id, l_name, l_English, l_Malay, l_Chinese, l_Tamil)
store_in_db(l_id, l_name, l_English, l_Malay, l_Chinese, l_Tamil)
