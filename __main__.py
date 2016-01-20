from loadImages import getDirectoryName, getImages, getProcessedImageName
from imageUtils import findROI, writeImage

def main():
	#get directory name
	directoryName = getDirectoryName()

	#get images
	imageFiles = getImages(directoryName)

	#loop through images
	for fileName in imageFiles:
		#finds rectangles, validates rectangles, finds region of interest, returns ROI
		processedImage = findROI(fileName)
		#writes image to folder "processed_" + original folder name
		processedImageName = getProcessedImageName(fileName)
		writeImage(processedImageName, processedImage)

		###################TODO###############################
	#CORE
	#3) detection of colored spot on center of image
	#4) quantify color of spot

	#SUPPLEMENTARY (non-issues atm)
	#1) deal with rounded rectangle
	#2) perspective correction

if __name__ == "__main__":
    main()