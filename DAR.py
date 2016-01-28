from loadImages import getProcessedImageName, writeInfo
from imageUtils import findROI, writeImage, spotQuantifier, showImage
from gooey import Gooey, GooeyParser
import pconfig
import sys
import os
import glob

@Gooey()
# class Unbuffered(object):
# 	def __init__(self, stream):
# 		self.stream = stream
# 	def write(self, data):
# 		self.stream.write(data)
# 		self.stream.flush()
# 	def __getattr__(self, attr):
# 		return getattr(self.stream, attr)
# sys.stdout = Unbuffered(sys.stdout)

def main():
	parser = GooeyParser(description="Compares Images!")
	parser.add_argument('directoryName', help="Name of the directory to process.", widget = "DirChooser")
	parser.add_argument('masterName', help="Name of the master image. Please put master image in the chosen directory.", widget = "FileChooser")
	parser.add_argument('--showOriginalImage', help = "(optional), default is False", nargs = "?", default = False)
	parser.add_argument('--showRegionOfInterest', help = "(optional), default is true", nargs = "?", default = True)
	parser.add_argument('--verbose', help = "Show Full Information, default is False", nargs = "?", default = False)
	# parser.add_argument('outputFileName', help="name of the output file")
	# parser.add_argument('extension', help = "(optional)name of extension (ex: JPG)")
	args = parser.parse_args()
	test_dirj = args.directoryName
	masterName = args.masterName
	showOriginalImage = args.showOriginalImage
	showRegionOfInterest = args.showRegionOfInterest
	if showOriginalImage == False:
		showOriginalImage = False
	else:
		showOriginalImage = True

	if showRegionOfInterest == True or showRegionOfInterest == "True" or showRegionOfInterest == "true":
		showRegionOfInterest = True
	else:
		showRegionOfInterest = False

	verbose = args.verbose
	if verbose != False or verbose != "false" or verbose != "False":
		verbose = True
	else:
		verbose = False


	# extensionFinal = pconfig.extension if (extension == "") else ("*" + extension)
	extensionFinal = pconfig.extension
	controlInfo = imageProcessor(masterName, test_dirj, showOriginalImage, showRegionOfInterest, verbose = verbose, control = True)
	controlScore = controlInfo[1]
	info = []
	for fileName in glob.glob(os.path.join(test_dirj, extensionFinal)):
		if fileName.lower() != os.path.join(test_dirj, masterName).lower():
			imageInfo = imageProcessor(fileName, test_dirj, showOriginalImage, showRegionOfInterest, controlScore = controlScore)
			info.append(imageInfo)
	print "Output File Name:" + writeInfo(info,test_dirj, controlInfo)
	print "done"

def imageProcessor(fileName, dirName, showOriginalImage, showRegionOfInterest, verbose = False, controlScore = 0, control = False):
	if control:
		print ""
		print "Beginning analysis on folder" + fileName
		print "CONTROL INFO"
	#imageInfo in form [fileName, rawScore, testIntensity, baselineIntensity,normalizedScore, pass/fail, controlScore]
	imageInfo = []
	#finds rectangles, validates rectangles, finds region of interest, returns processed image and bounding box info
	#optional parameter for ROI "drawCircle = true" to draw circle around ROI
	processedImage, bbInfo = findROI(os.path.join(dirName, fileName), showOriginalImage)
	#writes image to folder "processed_" + original folder name
	processedImageName = getProcessedImageName(fileName, dirName)
	#print processedImageName
	imageInfo.append(processedImageName)
	writeImage(processedImageName, processedImage)
	rawScore, testIntensity, baselineIntensity = spotQuantifier(processedImage, bbInfo, showRegionOfInterest)
	imageInfo.extend([rawScore, testIntensity, baselineIntensity])
	if not control:
		normalizedScore = rawScore - controlScore
		imageInfo.append(normalizedScore)
		if verbose:
			print "Raw Score: " + str(rawScore)
			print "Test Intensity: " + str(testIntensity)
			print "Baseline Intensity: " + str(baselineIntensity)
			print "Image: %s"% fileName
			print "Score: %i" % normalizedScore
			print ""
		else:
			print "Raw Score: " + str(rawScore)
			print "Image: %s"% fileName
			print ""
		imageInfo.append(controlScore)
	else:
		if verbose:
			print "Normalized score: The difference between the control score and the image's score. If the score is negative, the test image is darker than the control image."
			print "Control Score: The raw score for the master image. "
			print "Raw Score: The score for the image, calculated by the difference between the background(Baseline Intensity) and the dot (Test Intensity)."
			print "Test Intensity: The intensity of the dot (if no dot, calculated from center of ROI). "
			print "Baseline Intensity: Intensity of the background (calculated from inside the device's membrane ring)."
			print ""

			print "Raw Score: " + str(rawScore)
			print "Test Intensity: " + str(testIntensity)
			print "Baseline Intensity: " + str(baselineIntensity)
			print "Image Name: %s"% fileName
			print ""
			print "TEST IMAGES:"
			print ""
		else:
			print "Raw Score: " + str(rawScore)
			print "Image Name: %s"% fileName
			print ""
			print "TEST IMAGES:"
			print ""
	return imageInfo


if __name__ == "__main__":
	main()