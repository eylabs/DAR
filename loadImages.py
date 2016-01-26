import os, shutil, errno, fnmatch
import glob
import pconfig


def getProcessedImageName(fileName, dirName):
	img_dir = os.path.join(pconfig.IMG_DIR_PATH, "%s_processed" % dirName)
	try:
		os.makedirs(img_dir)
	except OSError:
		pass
	return "%s\%s_processed%s"%(img_dir, fileName.split(".")[0].split("\\")[-1], pconfig.extension[1:])

def writeInfo(info, dirName):
	outputFileDirectory = os.path.join(pconfig.MAIN_PATH, "results")
	try:
		os.makedirs(outputFileDirectory)
	except OSError:
		pass
	outputFileName = os.path.join(outputFileDirectory, "%s.txt" % (dirName))
	with open(outputFileName, "wb") as outfile:
		outfile.write("RESULTS: \n\n")
		for ii in info: #imageInfo
			outfile.write("%s\nNormalized Score: %i\nControl Score: %i, Raw Score: %i, Test Intensity: %i, Baseline Intensity: %i\n\n" % 
				(ii[0], ii[4], ii[5], ii[1], ii[2], ii[3]))
	return outputFileName