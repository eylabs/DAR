from loadImages import getDirectoryName, getImages
from imageUtils import findRectangles

def main():
	#get directory name
	directoryName = getDirectoryName()

	#get images
	imageFiles = getImages(directoryName)

	#loop through images
	for fileName in imageFiles:
		#find rectangles, validates rectangles, and returns coordinates
		findRectangles(fileName)


if __name__ == "__main__":
    main()