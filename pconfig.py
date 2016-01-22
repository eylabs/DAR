import os

my_images_path = ""

if not my_images_path:
	MAIN_PATH = os.getcwd()
else:
	MAIN_PATH = my_images_path

FOLDER_OF_INTEREST = "testImages1"
IMG_DIR_PATH = os.path.join(MAIN_PATH, "images")
IMG_PATH = os.path.join(IMG_DIR_PATH, FOLDER_OF_INTEREST)

CONTROL_IMG_DIR = os.path.join(IMG_DIR_PATH, "master")
CONTROL_FILE_NAME = os.path.join(CONTROL_IMG_DIR, "master.jpg")

# single extension
extension = "*.jpg"