import os, shutil, errno, fnmatch
import glob
import pconfig

#gets directory name based on paramters in pconfig
def getDirectoryName(sampleType):
	imageFileNames = []

	#positive
	if sampleType == 0:
		directoryName = os.path.join(pconfig.IMG_PATH, pconfig.POSITIVE_CONTROL)
		return os.path.join(directoryName, pconfig.extension)

	#negative
	if sampleType == 1:
		directoryName = os.path.join(pconfig.IMG_PATH, pconfig.NEGATIVE_CONTROL)
		return os.path.join(directoryName, pconfig.extension)

	#weak positive
	if sampleType == 2:
		directoryName = os.path.join(pconfig.IMG_PATH, pconfig.WEAK_POSITIVE_CONTROL)
		return os.path.join(directoryName, pconfig.extension)

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

def writeInfo(info, sampleType = 3):
	sampleTypeNames = ["positive", "negative", "weak positive", "other"]
	outputFileDirectory = os.path.join(pconfig.MAIN_PATH, "results")
	try:
		os.makedirs(outputFileDirectory)
	except OSError:
		pass
	outputFileName = os.path.join(outputFileDirectory, "%s_%s.txt" % (pconfig.FOLDER_OF_INTEREST, sampleTypeNames[sampleType]))
	with open(outputFileName, "wb") as outfile:
		outfile.write("RESULTS: \n\n")
		for ii in info: #imageInfo
			outfile.write("%s\nNormalized Score: %i\nControl Score: %i, Raw Score: %i, Test Intensity: %i, Baseline Intensity: %i\nResult: %s\n\n" % 
				(ii[0], ii[4], ii[6], ii[1], ii[2], ii[3], ii[5]))
	return outputFileName