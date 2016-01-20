import cv2
import numpy as np

#returns angle cosine given three points
def angle_cos(p0, p1, p2):
	d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
	return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )


#takes in a processed image, returns top rectangle, index of top rectangle, and all possiblerectangles
def findRectangles(processedImage):
	#possible rectangle finders
	possibleRectangles = possibleRectangleFinder(processedImage)

	#eliminate rectangles that are too large and picks top rectangle
	targetSize = (processedImage.shape[0]) * (processedImage.shape[1]) * 0.9
	#targetSize = "size of template rectangle" #alternative solution depending on UI later on
	
	topRectangleIndex = pickTopRectangle(possibleRectangles, targetSize)
	topRectangle = possibleRectangles[topRectangleIndex]
	return topRectangle, topRectangleIndex, possibleRectangles


#processes an image by applying a Gaussian blur
def imageBlur(image):
	blurred = cv2.GaussianBlur(image, (5, 5), 0)
	return blurred


#resize image for better viewing, takes in image, size of larger side
def imageResize(image, size):
	r = float(size) / image.shape[1]
	dim = (int(size), int(image.shape[0] * r))
	resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
	return resized


#returns index of largest rectangle smaller than the target size
def pickTopRectangle(possibleRectangles, targetSize):
	areas = [cv2.contourArea(rectangle) for rectangle in possibleRectangles]
	newAreas = []
	for area in areas:
		if area > targetSize:
			newAreas.append(0)
		else:
			newAreas.append(area)
	max_index = np.argmax(newAreas)
	return max_index


#returns possible squares
def possibleRectangleFinder(image):
	rectangles = []
	for gray in cv2.split(image):
		for thrs in xrange(0, 255, 26):
			if thrs == 0:
				bin = cv2.Canny(gray, 0, 50, apertureSize=5)
				bin = cv2.dilate(bin, None)
			else:
				retval, bin = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)
			bin, contours, hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
			for cnt in contours:
				cnt_len = cv2.arcLength(cnt, True)
				cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
				if len(cnt) == 4 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
					cnt = cnt.reshape(-1, 2)
					max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in xrange(4)])
					if max_cos < 0.1:
						rectangles.append(cnt)
	return rectangles


#shows image
def showImage(imageName, image):
	cv2.imshow(imageName, image)
	cv2.waitKey(0)
	cv2.destroyAllWindows

#writes image
def writeImage(imageName, image):
	cv2.imwrite(imageName,image)

#displays region of interest
def findROI(fileName):
	#read image
	image = cv2.imread(fileName)

	#image pre-processing (resize and blur)
	blurredImage = imageBlur(image)
	processedImage = imageResize(image, 2000)

	#finds rectangles and picks the top size
	topRectangle, topRectangleIndex, possibleRectangles = findRectangles(processedImage)

	#draws rectangles onto image
	cv2.drawContours(processedImage, possibleRectangles, topRectangleIndex, (0, 255, 0), 3 )

	#draws bounding rectangle
	x,y,w,h = cv2.boundingRect(topRectangle)
	cv2.rectangle(processedImage,(x,y),(x+w,y+h),(255,0,0),2)

	#draw circle
	midpoint = (int(x + w * 0.5), int(y + h * 0.5))
	cv2.circle(processedImage, midpoint, int(w * 0.2), (0,0,255), 3)
	resizedImage = imageResize(processedImage, 1000)
	showImage("rectangles", resizedImage)

	return resizedImage