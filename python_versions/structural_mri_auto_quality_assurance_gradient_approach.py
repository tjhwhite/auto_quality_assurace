#################################################################################################################################

# This program performs the automatic quality assessment on structural (T1) images and returns the gradient approach, as this was
# shown to be the most effective.

# Authors:		Tonya Jo Hanson White & Pierre-Olivier Quirion
# Date:			9 maart 2017
# Location: 	Rotterdam

#################################################################################################################################

# Import the packages that I need

import numpy as np
from numpy import genfromtxt

##--------------------------------------------------------------------------------------------------------------------------------
# THESE ARE ITEMS WHICH CAN EVENTUALLY BE CHANGED
##--------------------------------------------------------------------------------------------------------------------------------

# read in the data array, which has only numbers with the first column the idc, second the age, third sex 0=male, 1=female, the rest are values



# Load the paths

# Loop through each image in the path

# Register the image to native space and use the inverse transform matrix to place back the location of the brain  and in image space

# Use AFNI's 3Dedge3D to determine the edges of the image

# For each line in the region of interest, calculate the gradient along the edge

# Create an output datafile in the same order as the input path





class QaGradient(object):

    def __init__(self, path):
        self.path = path



    def run(self):
        pass




if __name__ == '__main__':
    dtidat = genfromtxt('.csv', delimiter=',')
