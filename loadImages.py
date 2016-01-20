import os, shutil, errno, fnmatch
import glob
import pconfig

#gets directory name based on paramters in pconfig
def getDirectoryName():
    imageFileNames = []
    directoryName = os.path.join(pconfig.IMG_PATH, pconfig.extension)
    return directoryName

#gets image files names
def getImages(directoryName):
    imageFiles = glob.glob(directoryName)
    print "Number of Files in %s: %i" % (directoryName, len(imageFiles))
    return imageFiles



# def findRectangles(img, fname, disp):
#     img_grey = img.greyscale()
#     blobs = img_grey.findBlobs(minsize = 100)
#     squares = blobs.filter([b.isSquare(0.1, 0.1) for b in blobs])

#     if len(squares) == 1:
#         squares.draw(color=Color.YELLOW, width=3)
#         # squares.draw(width=-1)
#         scrop = Image(img.size())
#         scrop = squares[0].crop()
#         scrop.drawText("Square Found", x=10,y=10, color=Color.YELLOW, fontsize=128)
#         scrop = scrop.applyLayers()

#         path, filen = os.path.split(fname)
#         sqrs_path = os.path.join(pconfig.squares_path, filen)
#         # print sqrs_path
#         scrop.save(sqrs_path, verbose=True)
#         findTemplateMatch(scrop, sqrs_path, disp) # give it squares image
#     else: 
#         print "sorry no match: %s " % fname

# def create_image(fname):
#     img = Image(fname)
#     return img, fname
    
# def process_images(path, extension):
#     directory = os.path.join(path, extension)  # can this work for multiple extensions?
#     files = glob.glob(directory)
#     print "Number of Files in %s: %i" % (path, len(files))
#     for file in (files):  # made a generator
#         yield file

# def locate_devices(disp):
# 	raw_file_gen = process_images(pconfig.IMG_PATH, pconfig.extension)
# 	img_gen = (create_image(s) for s in raw_file_gen)
# 	for img,fname in img_gen:
# 		print fname
# 		#findRectangles(img, fname, disp)