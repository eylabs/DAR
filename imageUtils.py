import cv2
import numpy as np

#shows image
def showImage(imageName, image):
	cv2.imshow(imageName, image)
	cv2.waitKey(0)
	cv2.destroyAllWindows

#returns angle cosine given three points
def angle_cos(p0, p1, p2):
	d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
	return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

#processes an image by resizing, 
def imageProcessing(image):
	#resize image for better viewing
	r = 1000.0 / image.shape[1]
	dim = (1000, int(image.shape[0] * r))
	resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

	#applies a Gaussian blur
	blurred = cv2.GaussianBlur(resized, (5, 5), 0)
	return blurred

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

#takes in an image, returns possible rectangles
def findRectangles(fileName):
	#read image
	image = cv2.imread(fileName)

	#image pre-processing (resize and blur)
	processedImage = imageProcessing(image)

	#possible rectangle finders
	possibleRectangles = possibleRectangleFinder(processedImage)

	#draws rectangles onto image
	cv2.drawContours(processedImage, possibleRectangles,0, (0, 255, 0), 3 )

	###################TODO###############################
	#1) validate each rectangle as possible candidate
	#2) identify region of interest for each device (based on physical measurements)
	#3) detection of colored spot on center of image
	#4) quantify color of spot

	showImage("rectangles", processedImage)

	return possibleRectangles





