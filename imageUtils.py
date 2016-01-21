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

#displays region of interest
def findROI(fileName, drawCircle = False):
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

	if drawCircle:
		#draw circle
		midpoint = (int(x + w * 0.5), int(y + h * 0.5))
		cv2.circle(processedImage, midpoint, int(w * 0.1), (0,0,255), 3)
	finalProcessedImage = processedImage.copy()

	resizedImage = imageResize(processedImage, 1000)
	#showImage(resizedImage)

	#returns resizedImage and information about the bounding box
	return finalProcessedImage, [x, y, w, h]

#processes an image by applying a Gaussian blur
def imageBlur(image):
	blurred = cv2.GaussianBlur(image, (5, 5), 0)
	return blurred


#crops image based on bounding box
def imageCrop(image, bbInfo):
	x = bbInfo[0]
	y = bbInfo[1]
	w = bbInfo[2]
	h = bbInfo[3]

	#crops image
	y1 = y + h * 0.5 - w * 0.1
	y2 = y + h * 0.5 + w * 0.1
	x1 = x + w * 0.4
	x2 = x + w * 0.6
	croppedImage = image[y1:y2, x1: x2]
	#showImage(croppedImage)
	return croppedImage


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
def showImage(image, imageName = "test"):
	cv2.imshow(imageName, image)
	cv2.waitKey(0)
	cv2.destroyAllWindows

#writes image
def writeImage(imageName, image):
	cv2.imwrite(imageName,image)

#must be grayscale
def imageInvert(image):
	if len(image.shape) == 2:
		return cv2.bitwise_not(image)
	else:
		print "image not inverted. grayscale needed"
		return image

#erodes edges of grayscale to make edges more sharp
def imageErode(image):
	kernel = np.ones((5,5),np.uint8)
	return cv2.erode(image, kernel ,iterations = 1)


#detects spot by cropping image, looking for spot, and quantifying spot intensity
def spotQuantifier(image, bbInfo):
	croppedImage = imageCrop(image, bbInfo)
	output = croppedImage.copy()
	gray = cv2.cvtColor(croppedImage, cv2.COLOR_BGR2GRAY) #changes croppedImage as well
	blurredGray = imageBlur(gray)
	blurredGrayInvert = imageInvert(blurredGray)
	erodedBlurredGrayInvert = imageErode(blurredGrayInvert)
	ret, processedImage = cv2.threshold(erodedBlurredGrayInvert, 127, 255, cv2.THRESH_BINARY)
	circles = cv2.HoughCircles(processedImage, cv2.HOUGH_GRADIENT, 1, 20, param1 = 100, param2 = 15, minRadius = 10)
	spotIntensity = 0
	# ensure at least some circles were found
	if circles is not None:
		# convert the (x, y) coordinates and radius of the circles to integers
		circles = np.round(circles[0, :]).astype("int")
	 
		# loop over the (x, y) coordinates and radius of the circles
		for (x, y, r) in circles:
			# draw the circle in the output image, then draw a rectangle
			# corresponding to the center of the circle
			cv2.circle(output, (x, y), r, (0, 255, 0), 4)
			cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
			print croppedImage.shape
			print (x,y,r)
			quantifyArea = croppedImage[y-20:y+20, x-20:x+20,]
			#showImage(quantifyArea)
			spotIntensity = np.average(quantifyArea)
			showImage(np.hstack([croppedImage, output]))
	return spotIntensity