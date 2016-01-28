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
	# parser.add_argument('outputFileName', help="name of the output file")
	# parser.add_argument('extension', help = "(optional)name of extension (ex: JPG)")
	args = parser.parse_args()
	test_dirj = args.directoryName
	masterName = args.masterName
	# extensionFinal = pconfig.extension if (extension == "") else ("*" + extension)
	extensionFinal = pconfig.extension
	controlInfo = imageProcessor(masterName, test_dirj, control = True)
	controlScore = controlInfo[1]
	info = []
	for fileName in glob.glob(os.path.join(test_dirj, extensionFinal)):
		if fileName.lower() != os.path.join(test_dirj, masterName).lower():
			imageInfo = imageProcessor(fileName, test_dirj, controlScore = controlScore)
			info.append(imageInfo)
	print "Output File Name:" + writeInfo(info,test_dirj, controlInfo)
	print "done"

def imageProcessor(fileName, dirName, controlScore = 0, control = False):
	if control:
		print ""
		print "Beginning analysis on folder" + fileName
		print "CONTROL INFO"
	#imageInfo in form [fileName, rawScore, testIntensity, baselineIntensity,normalizedScore, pass/fail, controlScore]
	imageInfo = []
	#finds rectangles, validates rectangles, finds region of interest, returns processed image and bounding box info
	#optional parameter for ROI "drawCircle = true" to draw circle around ROI
	processedImage, bbInfo = findROI(os.path.join(dirName, fileName))
	#writes image to folder "processed_" + original folder name
	processedImageName = getProcessedImageName(fileName, dirName)
	#print processedImageName
	imageInfo.append(processedImageName)
	writeImage(processedImageName, processedImage)
	rawScore, testIntensity, baselineIntensity = spotQuantifier(processedImage, bbInfo)
	imageInfo.extend([rawScore, testIntensity, baselineIntensity])
	if not control:
		normalizedScore = rawScore - controlScore
		imageInfo.append(normalizedScore)
		print "Raw Score: " + str(rawScore)
		print "Test Intensity: " + str(testIntensity)
		print "Baseline Intensity: " + str(baselineIntensity)
		print "Image: %s"% fileName
		print "Score: %i" % normalizedScore
		print ""
		imageInfo.append(controlScore)
	else:
		print "Normalized score: The difference between the control score and the image's score. If the score is negative, the test image is darker than the control image."
		print "Control Score: The raw score for the master image. "
		print "Raw Score: The score for the image, calculated by the difference between the background(Baseline Intensity) and the dot (Test Intensity)."
		print "Test Intensity: The intensity of the dot (if no dot, calculated from center of ROI). "
		print "Baseline Intensity: Intensity of the background (calculated from inside the device's membrane ring)."
		print ""

		print "Test Intensity: " + str(testIntensity)
		print "Baseline Intensity: " + str(baselineIntensity)
		print "Image Name: %s"% fileName
		print "Score: %i"%(rawScore)
		print ""
	return imageInfo


if __name__ == "__main__":
	main()