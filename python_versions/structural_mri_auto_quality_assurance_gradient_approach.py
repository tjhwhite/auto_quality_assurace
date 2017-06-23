#################################################################################################################################

# This program performs the automatic quality assessment on structural (T1) images and returns the gradient approach, as this was
# shown to be the most effective.

# Authors:		Tonya Jo Hanson White & Pierre-Olivier Quirion
# Date:			9 maart 2017
# Location: 	Rotterdam

#################################################################################################################################
__version__ = 0.1

import argparse
import os
import subprocess
import sys
import uuid

"""
Load the paths

Loop through each image in the path

Register the image to native space and use the inverse transform matrix to place back the location of the brain  and in image space

Use AFNI's 3Dedge3D to determine the edges of the image

For each line in the region of interest, calculate the gradient along the edge

Create an output datafile in the same order as the input path
"""

PROJECT_DIR = os.path.dirname(__file__)


class QaGradient(object):

    TMP_DIR = '/tmp'

    def __init__(self, image_path, registered_path=None, edge_path=None, output_dir=None):

        self.image_path = image_path
        self.uid = 33  # uuid.uuid4()
        self.image = None
        self.t1_reference = os.path.join(PROJECT_DIR, 'data', 'MNI152_T1_1mm.nii.gz')

        if output_dir is None:
            self.ouput_dir = self.TMP_DIR
        else:
            self.ouput_dir = output_dir

        if registered_path is None:
            self.registered_path = os.path.join(self.ouput_dir,
                                                'registered_{}_{}'.
                                                format(self.uid, os.path.basename(self.image_path)))
            if self.registered_path.endswith('.nii'):
                self.registered_path = '{}.gz'.format(self.registered_path)

        else:
            self.registered_path = registered_path

        if edge_path is None:
            self.edge_path = os.path.join(self.ouput_dir,
                                                'edge_{}_{}'.
                                                format(self.uid, os.path.basename(self.image_path)))
            if self.edge_path.endswith('.nii'):
                self.edge_path = '{}.gz'.format(self.edge_path)

        else:
            self.edge_path = edge_path

        self.fsl_laucher = os.path.join(PROJECT_DIR, 'launch_fsl.sh')
        self.afni_laucher = os.path.join(PROJECT_DIR, 'launch_afni.csh')

        self.mean_gradient = None


    def fsl_flirt(self,in_file=None, out_file=None, reference=None):
        """ Runs FSL flirt with a selected list of options     
        
        :param in_file: 
        :param out_file: 
        :param reference: 
        :return: 
        """

        flrtcmd = [self.fsl_laucher, 'flirt', '-in', in_file, '-ref', reference, '-omat' matrix_transform, '-out', out_file, '-searchrx' min_angle max_angle, '-searchry' min_angle max_angle, '-searchrz' min_angle max_angle, ]

        subprocess.call(flrtcmd)

	def fsl_invmat(self,in_file=None, out_file=None):
	    """ Runs FSL flirt with a selected list of options     

	    :param in_file: matrix transform
	    :param out_file: inverse matrix transform
	    :return: 
	
		convert_xfm -omat <outmat> -inverse <inmat>
	        """

		invmat = [self.fsl_laucher, 'convert_xfm', '-omat', out_file, '-inverse', in_file, ]

		subprocess.call(invmat)

    def afni_3dedge3(self, in_file=None, out_file=None):
        """Running Afni 3deges3

        :param in_file: 
        :param out_file: 
        :param reference: 
        :return: 
        """
        a_3dedge3 = [self.afni_laucher, '3dedge3', '-input', in_file, '-prefix', out_file]

        subprocess.call(a_3dedge3)

    def _register(self):
        """
        Register the image to native space and use the inverse 
        transform matrix to place back the location of the brain and
        in image space

        :return: 
        """

        self.fsl_flirt(in_file=self.image_path, reference=self.t1_reference, out_file=self.registered_path)

    def deform_mask(self):
        pass

    def _edges(self):
        """
        Use AFNI's 3Dedge3D to determine the edges of the image
        :return: 
        """
        self.afni_3dedge3(in_file=self.registered_path, out_file=self.edge_path)

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

        return self.mean_gradient


def main(args=None):

    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(description='QA gradient measures the mean of gradient '
                                                 'of signal in a regions on the back of the head')

    parser.add_argument("--inputs", "-i", type=str, required=True,
                        help='A nifti file or a directory including nifti files')

    parsed = parser.parse_args(args)

    all_qa = []
    if os.path.isfile(parsed.inputs):
        all_qa.append(QaGradient(parsed.inputs))
    elif os.path.dirname(parsed.inputs):
        all_file = [nii for nii in os.listdir(parsed.inputs) if nii.endswith(".nii.gz") or nii.endswith(".nii")]
        for f in all_file:
            all_qa.append(QaGradient(os.path.join(parsed.inputs, f)))

    for qa in all_qa:
        qa.run()

if __name__ == '__main__':
    main()
