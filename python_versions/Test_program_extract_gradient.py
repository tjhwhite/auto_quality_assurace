#!/usr/bin/env python
# encoding: utf-8
"""
Test_new_gradient.py

Created by Tonya White on 2017-06-24.
Copyright (c) 2017 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import numpy as np
import nibabel as nib
import matplotlib as ml
import matplotlib.pyplot as plt


# Load the three different images to test, first define the paths

img_path_orig = '/Users/tonya/Documents/MRI_Data/Structural/t1_101704.nii.gz'
img_path_edge = '/Users/tonya/Documents/MRI_Data/Structural/edge_66_t1_101704.nii.gz'
img_path_roi = '/Users/tonya/Documents/MRI_Data/Structural/roi_66_t1_101704.nii.gz'

img_1 = nib.load(img_path_orig)
img = img_1.get_data()

#img_2 = nib.load(img_path_edge)
#edge = img_2.get_data()

edge = img > 2000

img_3 = nib.load(img_path_roi)
roi = img_3.get_data()

simg = img.shape

third = int(roi.shape[0]/3)

xmin_sum = roi[0:third].sum(0)
xmax_sum = roi[2*third:-1].sum(0)

imgplot = plt.imshow(xmax_sum)
plt.show()
vals_left = 0
vals_right = 0
count_left = 0 
count_right = 0

for y in xrange(0,roi.shape[1]):
	for z in xrange(0,roi.shape[2]):
		if xmin_sum[y,z] > 0:
			icount = 0
			while not edge[icount,y,z]:
				icount = icount + 1
			if icount > 4:
				vals_left = vals_left + (img[icount+1,y,z] - img[icount-4,y,z])
				count_left = count_left + 1
		if xmax_sum[y,z] > 0:
			icount = roi.shape[0] - 1 
			while not edge[icount,y,z]:
				icount = icount - 1
			if roi.shape[0] - icount > 5:
				vals_right = vals_right + (img[icount-1,y,z] - img[icount+4,y,z])
				count_right = count_right + 1



# Calculate the gradient value for the right and the left side of the brain
grad_left = vals_left / count_left
grad_right = vals_right / count_right






