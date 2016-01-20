import cv2
import numpy as np
from matplotlib import pyplot as plt
#import pconfig

def showImage(image):
	cv2.imshow('res', image)
	cv2.waitKey(0)
	cv2.destroyAllWindows

def main():
	trial4()

def angle_cos(p0, p1, p2):
	d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
	return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

def find_squares(img):
	img = cv2.GaussianBlur(img, (5, 5), 0)
	squares = []
	for gray in cv2.split(img):
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
						squares.append(cnt)
	return squares

def trial4():
	from glob import glob
	for fn in glob('./data/*.jpg'):
		image = cv2.imread(fn)
		r = 1000.0 / image.shape[1]
		dim = (1000, int(image.shape[0] * r))
		resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
		squares = find_squares(resized)

		cv2.drawContours( resized, squares, 0, (0, 255, 0), 3 )
		#threshold the image 
		print squares
		print len(squares)
		print squares[0]

		cv2.imshow('squares', resized)
		ch = 0xFF & cv2.waitKey()
		if ch == 27:
			break
	cv2.destroyAllWindows()

def trial3():
	image = cv2.imread("20160119_115236.jpg")
	r = 1000.0 / image.shape[1]
	dim = (1000, int(image.shape[0] * r))
	resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
	output = resized.copy()
	img2gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
	showImage(output)
	showImage(img2gray)
	ret,thresh = cv2.threshold(img2gray,127,255,0)
	showImage(thresh)

	kernel = np.ones((5,5),np.float32)/25
	dst = cv2.filter2D(thresh,-1,kernel)
	showImage(dst)
	edges = cv2.Canny(dst,0,10)
	plt.subplot(121),plt.imshow(dst,cmap = 'gray')
	plt.title('Original Image'), plt.xticks([]), plt.yticks([])
	plt.subplot(122),plt.imshow(edges,cmap = 'gray')
	plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
	plt.show()

	im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	cv2.drawContours(im2, contours, -1, (0,255,0), 3)
	#showImage(im2)






#circle detection
def trial2():
	#load image, clone, convert to grayscale
	image = cv2.imread("circle.jpg")

	output = image.copy()
	img2gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	#detect circles
	circles = cv2.HoughCircles(img2gray, cv2.HOUGH_GRADIENT, 1.2, 100)
	 
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
	 
		# show the output image
		cv2.imshow("output", np.hstack([image, output]))
		cv2.waitKey(0)

#superimposing images
def trial1():
	# Load two images
	img1 = cv2.imread('steph_curry.jpg')
	img2 = cv2.imread('MIT_logo.jpg')

	# I want to put logo on top-left corner, So I create a ROI
	rows,cols,channels = img2.shape
	roi = img1[0:rows, 0:cols ]
	showImage(roi)

	# Now create a mask of logo and create its inverse mask also
	img2gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
	showImage(img2gray)
	ret, mask = cv2.threshold(img2gray, 80, 255, cv2.THRESH_BINARY)
	showImage(mask)
	mask_inv = cv2.bitwise_not(mask)
	showImage(mask_inv)


	# Now black-out the area of logo in ROI
	img1_bg = cv2.bitwise_and(roi,roi,mask = mask)
	showImage(img1_bg)

	# Take only region of logo from logo image.
	img2_fg = cv2.bitwise_and(img2,img2,mask = mask_inv)
	showImage(img2_fg)
	img2_fg_mod = 255 - img2_fg
	showImage(img2_fg_mod)

	# Put logo in ROI and modify the main image
	dst = cv2.add(img1_bg,img2_fg_mod)
	img1[0:rows, 0:cols ] = dst

	cv2.imshow('res',img1)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

main()