#################################################################################################################################

# This program performs the automatic quality assessment on structural (T1) images and returns the gradient approach, as this was
# shown to be the most effective.

# Authors:		Tonya Jo Hanson White & Pierre-Olivier Quirion
# Date:			9 maart 2017
# Location: 	Rotterdam

#################################################################################################################################

__version__ = 0.1

import os

import numpy as np
import nipype
import nibabel
import subprocess

"""
Load the paths

Loop through each image in the path

Register the image to native space and use the inverse transform matrix to place back the location of the brain  and in image space

Use AFNI's 3Dedge3D to determine the edges of the image

For each line in the region of interest, calculate the gradient along the edge

Create an output datafile in the same order as the input path
"""

PROJECT_DIR,file_name = os.path.split(__file__)



class Qa(object):

    def __init__(self, path):

        self.path = path
        self.image = None
        self.t1_reference = os.path.join(PROJECT_DIR, 'data', 'MNI152_T1_1mm.nii.gz')
        self.output_type = "NIFTI_GZ"

        self.fsl_laucher = os.path.join(PROJECT_DIR, 'launch_fsl.sh')
        self.afni_laucher = os.path.join(PROJECT_DIR, 'launch_afni.sh')


    def flirt(self,in_file=None, out_file=None, reference=None):
        """
        
        :param in_file: 
        :param out_file: 
        :param reference: 
        :return: 
        """

        flrtcmd = [self.fsl_laucher, 'flirt', '-in', in_file, '-ref', reference, '-omat' matrix_transform, '-out', out_file, '-searchrx' min_angle max_angle, '-searchry' min_angle max_angle, '-searchrz' min_angle max_angle, ]

        subprocess.call(flrtcmd)

    def _register(self):
        """
        Register the image to native space and use the inverse 
        transform matrix to place back the location of the brain and
        in image space

        :return: 
        """

        self.flirt(in_file=self.image)


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

        self._register()
        self._edges()
        self._gradient()

        return self.gradient




if __name__ == '__main__':
    # read in the data array, which has only numbers with the first column the idc, second the age, third sex 0=male, 1=female, the rest are values

#    dtidat = np.genfromtxt('.csv', delimiter=',')


    inputs = '/home/poquirion/presentation/brainhack/ohbm_2017/projects/inputs'
    t1_paths = os.listdir(inputs)

    gradiants = []

    for t1_path in t1_paths:
        # path = d ## get that right

        qa = Qa(os.path.join(inputs, t1_path))

        qa._register()


        # gradiants.append(qa.run())

    import pprint
    pprint.pprint(gradiants)