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

def writeInfo(info, dirName, controlInfo):
	outputFileDirectory = os.path.join(pconfig.MAIN_PATH, "results")
	try:
		os.makedirs(outputFileDirectory)
	except OSError:
		pass
	outputFileName = os.path.join(outputFileDirectory, "%s.txt" % (dirName))
	with open(outputFileName, "wb") as outfile:
		outfile.write("CONTROL INFO: \n\n")
		outfile.write("Score: %i, Test Intensity: %i, Baseline Intensity %i\n" % (controlInfo[1], controlInfo[2], controlInfo[3]))
		outfile.write("RESULTS: \n\n")
		outfile.write("Normalized score: The difference between the control score and the image's score. If the score is negative, the test image is darker than the control image.\n")
		outfile.write("Control Score: The raw score for the master image. \n")
		outfile.write("Raw Score: The score for the image, calculated by the difference between the background(Baseline Intensity) and the dot (Test Intensity).\n")
		outfile.write("Test Intensity: The intensity of the dot (if no dot, calculated from center of ROI).\n ")
		outfile.write("Baseline Intensity: Intensity of the background (calculated from inside the device's membrane ring).\n\n")
		for ii in info: #imageInfo
			outfile.write("%s\nNormalized Score: %i\nControl Score: %i, Raw Score: %i, Test Intensity: %i, Baseline Intensity: %i\n\n" % 
				(ii[0], ii[4], ii[5], ii[1], ii[2], ii[3]))
	return outputFileName