from loadImages import getDirectoryName, getImages, getProcessedImageName, writeInfo
from imageUtils import findROI, writeImage, spotQuantifier, showImage

def main():
	#get directory name
	directoryName = getDirectoryName()

	#get images
	imageFiles = getImages(directoryName)

	#information to be written
	info = []

	#loop through images
	for fileName in imageFiles:
		#info for each image in form [fileName, score, testIntensity, baselineIntensity, result]
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
		score, testIntensity, baselineIntensity = spotQuantifier(processedImage, bbInfo)
		imageInfo.extend([score, testIntensity, baselineIntensity])
		print score
		if score < 40:
			print "POSITIVE"
			print ""
			imageInfo.append("POSITIVE")
		else:
			print "NEGATIVE"
			print ""
			imageInfo.append("NEGATIVE")
		info.append(imageInfo)

	#writes to another file
	print writeInfo(info)
	print "done"


if __name__ == "__main__":
    main()