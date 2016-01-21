import os

my_images_path = ""

if not my_images_path:
	MAIN_PATH = os.getcwd()
else:
	MAIN_PATH = my_images_path

FOLDER_OF_INTEREST = "testImages"
IMG_DIR_PATH = os.path.join(MAIN_PATH, "images")
IMG_PATH = os.path.join(IMG_DIR_PATH, FOLDER_OF_INTEREST)

# single extension
extension = "*.jpg"