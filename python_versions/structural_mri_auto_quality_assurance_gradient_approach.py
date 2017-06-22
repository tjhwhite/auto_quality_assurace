#################################################################################################################################

# This program performs the automatic quality assessment on structural (T1) images and returns the gradient approach, as this was
# shown to be the most effective.

# Authors:		Tonya Jo Hanson White & Pierre-Olivier Quirion
# Date:			9 maart 2017
# Location: 	Rotterdam

#################################################################################################################################

__version__ = 0.1

import numpy as np
from numpy import genfromtxt
import nipype


"""
Load the paths

Loop through each image in the path

Register the image to native space and use the inverse transform matrix to place back the location of the brain  and in image space

Use AFNI's 3Dedge3D to determine the edges of the image

For each line in the region of interest, calculate the gradient along the edge

Create an output datafile in the same order as the input path
"""





class Qa(object):

    def __init__(self, path):
        self.path = path

    def _register(self):
        """
        Register the image to native space and use the inverse 
        transform matrix to place back the location of the brain and
        in image space

        :return: 
        """
        pass

        

    def _edges(self):
        """
        Use AFNI's 3Dedge3D to determine the edges of the image
        :return: 
        """
        pass


    def _gradient(self):
        """
        For each line in the region of interest, calculate the gradient
        along the edge

        :return: 
        """
        pass


    def run(self):
        """
        
        :return: 
        """
        pass

class Execute():
    def __init__(self):
        pass

if __name__ == '__main__':
    # read in the data array, which has only numbers with the first column the idc, second the age, third sex 0=male, 1=female, the rest are values

    dtidat = genfromtxt('.csv', delimiter=',')

    gradiants = []

    for d in dtidat:
        path = d ## get that right

        qa = Qa(path)


        gradiants.append(qa.run())

    import pprint
    pprint.pprint(gradiants)