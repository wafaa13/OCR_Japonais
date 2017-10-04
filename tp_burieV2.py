# Image Gaussien
import sys
import cv2
import os
import numpy as np
from matplotlib import pyplot as plt
import imghdr
from scipy import ndimage 
import scipy.misc
from astropy.io import fits
from astropy.utils.data import get_pkg_data_filename
from astropy.convolution import Gaussian2DKernel
from scipy.signal import convolve as scipy_convolve
from astropy.convolution import convolve
from scipy import signal as sg
import sift
from scipy import ndimage as ndi

def applicationOfFilter(img, folder):

	# ==============================
	# ========== OPEN IMG ==========
	# ==============================

	# Ovrir image 
	img = openImage(folder, img)
	no = openImage(folder, "no.png")
	no2 = openImage(folder, "no2.png")
	a = openImage(folder, "a.png")
	shi = openImage(folder, "shi.png")
	tsu = openImage(folder, "tsu.png")
	nu = openImage(folder, "nu.png")

	# Image noir et blanc
	imgBW = getNBImage(img)
	no = getNBImage(no)
	no2 = getNBImage(no2)
	a = getNBImage(a)
	shi = getNBImage(shi)
	tsu = getNBImage(tsu)
	nu = getNBImage(nu)

	# Save image
	scipy.misc.imsave('otsu.png', imgBW)


	# image = 1
	# tab = []
	# width, height = imgBW.shape
	# for i in range(0, width)
	# 	for j in range(0, height)
	# 		if imgBW[i, j] = 0
	# 			xmin, ymin, xmax, ymax = getXYMinMax(width, height, 0, 0)
	# 			tab[]

	# plt.hist(img.ravel(),256,[0,256])
	# plt.show()
	# plt.imshow(im_med)
	# plt.show()

	# ==============================
	# ========= TRAITEMENT =========
	# ==============================

	# Pourcentage de noir et blanc 
	noHist = getHistGreyImage(no)
	aHist = getHistGreyImage(a)
	shiHist = getHistGreyImage(shi)
	tsuHist = getHistGreyImage(tsu)
	nuHist = getHistGreyImage(nu)

	# Create dictionnary
	percentTab = {}

	# Put values in a dictionnary
	percent = noHist[0]/(noHist[0]+noHist[255])*100
	percentTab["no"] = percent[0]
	percent = aHist[0]/(aHist[0]+aHist[255])*100
	percentTab["a"] = percent[0]
	percent = shiHist[0]/(shiHist[0]+shiHist[255])*100
	percentTab["shi"] = percent[0]
	percent = tsuHist[0]/(tsuHist[0]+tsuHist[255])*100
	percentTab["tsu"] = percent[0]
	percent = nuHist[0]/(nuHist[0]+nuHist[255])*100
	percentTab["nu"] = percent[0]

	print ""
	print "tableau de poucentage de noir : "
	print percentTab
	print "on peut dire que si c'est en dessous de 13, c'est shi ou tsu, sinon c'est a, nu ou no"
	print ""

	# SIFT
	# compare(no, no2)

	return 0

def getNBImage(img):
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	# Otsu
	img = img.astype(np.uint8)
	ret, thresh = cv2.threshold(img,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
	NBimage = np.invert(thresh)
	return NBimage

def compare(img1, img2):
	# copyMatrix = no
	# sift = cv2.xfeatures2d.SIFT_create() 
	# kp, des = sift.detectAndCompute(no,None)
	# img = cv2.drawKeypoints(no,kp, copyMatrix)
	# cv2.imwrite('sift_keypoints_no.jpg',img)

	# copyMatrix2 = no2
	# kp2, des2 = sift.detectAndCompute(no2,None)
	# img2 = cv2.drawKeypoints(no2,kp2, copyMatrix2)
	# cv2.imwrite('sift_keypoints_no2.jpg',img2)

	# Initiate SIFT detector
	sift = cv2.xfeatures2d.SIFT_create() 

	# find the keypoints and descriptors with SIFT
	kp1,des1 = sift.detectAndCompute(img1,None)
	kp2,des2 = sift.detectAndCompute(img2,None)
	# FLANN parameters
	FLANN_INDEX_KDTREE = 1
	index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
	search_params = dict(checks=50)   # or pass empty dictionary
	flann = cv2.FlannBasedMatcher(index_params,search_params)
	matches = flann.knnMatch(des1,des2,k=2)
	# Need to draw only good matches, so create a mask
	matchesMask = [[0,0] for i in xrange(len(matches))]
	# ratio test as per Lowe's paper
	for i,(m,n) in enumerate(matches):
	    if m.distance < 0.7*n.distance:
	        matchesMask[i]=[1,0]
	draw_params = dict(matchColor = (0,255,0),
	                   singlePointColor = (255,0,0),
	                   matchesMask = matchesMask,
	                   flags = 0)
	img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,matches,None,**draw_params)
	cv2.imwrite('sift_keypoints_compare.jpg',img3)


# Return image opened
def openImage(folder,filename):
	return cv2.imread(os.path.join(folder,filename))

# Return the 3 histogram RGB
def getHistColorImage(img):
	histBlue = cv2.calcHist([img],[0],None,[16],[0,256])
	histGreen = cv2.calcHist([img],[1],None,[16],[0,256])
	histRed = cv2.calcHist([img],[2],None,[16],[0,256])
	return [histBlue, histGreen, histRed]

# Return the 3 histogram RGB
def getHistGreyImage(img):
	hist = cv2.calcHist([img],[0],None,[256],[0,256])
	return hist


# Line : python tp_burie.py img.jpg
img = str(sys.argv[1])
folder = str(sys.argv[2])
applicationOfFilter(img, folder)
