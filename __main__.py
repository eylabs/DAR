from loadImages import getDirectoryName, getImages, getProcessedImageName, writeInfo
from imageUtils import findROI, writeImage, spotQuantifier, showImage
import pconfig

def main():
	#get directory name
	directoryName = getDirectoryName()

	#get images
	imageFiles = getImages(directoryName)

	#information to be written
	info = []
	controlScore = imageProcessor(pconfig.CONTROL_FILE_NAME, control = True)[1]

	print ""
	print "TEST SCORES:"
	#loop through images
	for fileName in imageFiles:
		#info for each image in form [fileName, rawScore, testIntensity, baselineIntensity, normalizedScore, result]
		imageInfo = imageProcessor(fileName, controlScore = controlScore)
		info.append(imageInfo)

	#writes to another file
	print writeInfo(info)
	print "done"

def imageProcessor(fileName, controlScore = 0, control = False):
	if control:
		print ""
		print "CONTROL INFO"
	imageInfo = []
	#finds rectangles, validates rectangles, finds region of interest, returns processed image and bounding box info
	#optional parameter for ROI "drawCircle = true" to draw circle around ROI
	processedImage, bbInfo = findROI(fileName)
	#writes image to folder "processed_" + original folder name
	processedImageName = getProcessedImageName(fileName)
	print processedImageName
	imageInfo.append(processedImageName)
	writeImage(processedImageName, processedImage)

	#usees processed image to
	rawScore, testIntensity, baselineIntensity = spotQuantifier(processedImage, bbInfo)
	imageInfo.extend([rawScore, testIntensity, baselineIntensity])
	print rawScore
	if not control:
		normalizedScore = abs(rawScore - controlScore)
		imageInfo.append(normalizedScore)
		if normalizedScore < 40:
			print "POSITIVE"
			print ""
			imageInfo.append("POSITIVE")
		else:
			print "NEGATIVE"
			print ""
			imageInfo.append("NEGATIVE")
	return imageInfo

if __name__ == "__main__":
    main()