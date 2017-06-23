#################################################################################################################################

# This program reads in a standard brain and creates a mask to be used in the auto Q/A program for the inverse transform into
# native image space

# Authors:		Tonya Jo Hanson White & Pierre-Olivier Quirion
# Date:			22 juni 2017
# Location: 	Vancouver, BC

#################################################################################################################################

# Import the packages that I need

import os
import numpy as np
import nibabel as nib
import matplotlib as ml
import matplotlib.pyplot as plt

##--------------------------------------------------------------------------------------------------------------------------------
# THESE ARE ITEMS WHICH CAN EVENTUALLY BE CHANGED

img_path = '/usr/local/fsl/data/standard/MNI152_T1_1mm.nii.gz'

##--------------------------------------------------------------------------------------------------------------------------------


img = nib.load(img_path)
hdr = img.header
data = img.get_data()
a = data.shape

# Look at the image in 2D
img2d_cor = data[:,109,:]
plt.imshow(img2d)
plt.show()

img2d_sag = data[91,:,:]
plt.imshow(img2d_sag)
plt.show()

img2d_ax = data[:,:,91]
plt.imshow(img2d_ax)
plt.show()

imgthresh = data > 3000
itr = imgthresh.astype(int)

img2d_bin_cor = itr[:,109,:]
plt.imshow(img2d_bin_cor)
plt.show()

slabarr = np.zeros([182,218,182])

for x in xrange(0,181):
	for y in xrange(60,160):
		for z in xrange(81,161):
			if itr[x,y,z] == 0 :
				slabarr[x,y,z] = 1


imgdemo = slabarr + itr 



