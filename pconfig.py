import os

my_images_path = ""

if not my_images_path:
	MAIN_PATH = os.getcwd()
else:
	MAIN_PATH = my_images_path

FOLDER_OF_INTEREST = "simpleComparison"
POSITIVE_CONTROL = "masterPositive"
NEGATIVE_CONTROL = "masterNegative"
WEAK_POSITIVE_CONTROL = "masterWeakPositive"
IMG_DIR_PATH = os.path.join(MAIN_PATH, "images")
IMG_PATH = os.path.join(IMG_DIR_PATH, FOLDER_OF_INTEREST)
CONTROL_IMG_DIR = os.path.join(IMG_DIR_PATH, "master")
POS_CONTROL_FILE_NAME = os.path.join(CONTROL_IMG_DIR, "masterPositive.jpg")
NEG_CONTROL_FILE_NAME = os.path.join(CONTROL_IMG_DIR, "masterNegative.jpg")
WEAK_POS_CONTROL_FILE_NAME = os.path.join(CONTROL_IMG_DIR, "masterWeakPositive.jpg")

IMAGE1 = os.path.join(IMG_PATH, "image1.jpg")
IMAGE2 = os.path.join(IMG_PATH, "image2.jpg")

def controlFileName(sampleType):
	#positive
	if sampleType == 0:
		return POS_CONTROL_FILE_NAME
	if sampleType == 1:
		return NEG_CONTROL_FILE_NAME
	if sampleType == 2:
		return WEAK_POS_CONTROL_FILE_NAME



# single extension
extension = "*.jpg"