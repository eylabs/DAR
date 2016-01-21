import os, shutil, errno, fnmatch
import glob
import pconfig

#gets directory name based on paramters in pconfig
def getDirectoryName():
	imageFileNames = []
	directoryName = os.path.join(pconfig.IMG_PATH, pconfig.extension)
	return directoryName

#gets image files names
def getImages(directoryName):
	imageFiles = glob.glob(directoryName)
	print "Number of Files in %s: %i" % (directoryName, len(imageFiles))
	return imageFiles

def getProcessedImageName(fileName):
	#tries to mkdir
	img_dir = os.path.join(pconfig.IMG_DIR_PATH, "%s_processed" % (pconfig.FOLDER_OF_INTEREST))
	try:
		os.makedirs(img_dir)
	except OSError:
		pass
	#creates new file name
	return "%s\%s_processed%s"%(img_dir, fileName.split(".")[0].split("\\")[-1], pconfig.extension[1:])