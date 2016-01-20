import os

my_images_path = ""

if not my_images_path:
	MAIN_PATH = os.getcwd()
else:
	MAIN_PATH = my_images_path

IMG_PATH = os.path.join(os.path.join(MAIN_PATH, "images"), "dark")

# single extension
extension = "*.jpg"