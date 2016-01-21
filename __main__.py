from loadImages import getDirectoryName, getImages, getProcessedImageName
from imageUtils import findROI, writeImage, spotQuantifier, showImage

def main():
	#get directory name
	directoryName = getDirectoryName()

	#get images
	imageFiles = getImages(directoryName)

	#loop through images
	for fileName in imageFiles:
		#finds rectangles, validates rectangles, finds region of interest, returns processed image and bounding box info
		#optional parameter for ROI "drawCircle = true" to draw circle around ROI
		processedImage, bbInfo = findROI(fileName)
		#writes image to folder "processed_" + original folder name
		processedImageName = getProcessedImageName(fileName)
		writeImage(processedImageName, processedImage)

		#usees processed image to
		score = spotQuantifier(processedImage, bbInfo)
		print score

		###################TODO###############################
	#CORE
	#4) quantify color of spot

	#SUPPLEMENTARY (non-issues atm)
	#1) deal with rounded rectangle
	#2) perspective correction

if __name__ == "__main__":
    main()