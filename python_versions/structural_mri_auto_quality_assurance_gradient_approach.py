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
import logging
import nibabel

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
    """QaGradian is a class that take a structural image as an input and outputs the mean of edge gradian at 
    the edge of the skull within an ROI
    
    """
    TMP_DIR = '/tmp'

    def __init__(self, original_image_path, registered_image_path=None, edge_path=None, output_dir=None,
                 matrix_path=None, searchrx=(-90, 90), searchry=(-90, 90), searchrz=(-90, 90),
                 roi_user_space=None, rev_matrix_path=None, standard_space_image_path=None,
                 verbose=1, roi_standard_space=None, clean_intermediate=True):

        self.original_image_path = original_image_path
        self.uid = 2  # uuid.uuid4()
        self.image = None

        if standard_space_image_path is None:
            self.standard_space_image_path = os.path.join(PROJECT_DIR, 'data', 'MNI152_T1_1mm.nii.gz')
        else:
            self.standard_space_image_path = standard_space_image_path
        if roi_standard_space is None:
            self.roi_standard_space = os.path.join(PROJECT_DIR, 'data', 'auto_qa_roi_definition.nii.gz')
        else:
            self.roi_standard_space = roi_standard_space
        if output_dir is None:
            self.ouput_dir = self.TMP_DIR
        else:
            self.ouput_dir = output_dir
        if registered_image_path is None:
            self.registered_registered_path = os.path.join(self.ouput_dir,
                                                'registered_{}_{}'.
                                                           format(self.uid, os.path.basename(self.original_image_path)))
            if self.registered_registered_path.endswith('.nii'):
                self.registered_registered_path = '{}.gz'.format(self.registered_registered_path)

        else:
            self.registered_registered_path = registered_image_path
        if edge_path is None:
            self.edge_path = os.path.join(self.ouput_dir,
                                                'edge_{}_{}'.
                                          format(self.uid, os.path.basename(self.original_image_path)))
            if self.edge_path.endswith('.nii'):
                self.edge_path = '{}.gz'.format(self.edge_path)

        else:
            self.edge_path = edge_path
        if matrix_path is None:
            self.matrix_path = os.path.join(self.ouput_dir,
                                                'matrix_{}_{}'.
                                            format(self.uid, os.path.basename(self.original_image_path)))
            self.matrix_path = '{}.xfm'.format(os.path.splitext(self.matrix_path)[0])

        else:
            self.matrix_path = matrix_path
        if rev_matrix_path is None:
            self.rev_matrix_path = os.path.join(self.ouput_dir,
                                                'rev_matrix_{}_{}'.
                                                format(self.uid, os.path.basename(self.original_image_path)))
            self.rev_matrix_path = '{}.xfm'.format(os.path.splitext(self.rev_matrix_path)[0])
        else:
            self.matrix_path = matrix_path
        if roi_user_space is None:
            self.roi_user_space = os.path.join(self.ouput_dir,
                                                'roi_{}_{}'.
                                               format(self.uid, os.path.basename(self.original_image_path)))
            if self.roi_user_space.endswith('.nii'):
                self.roi_user_space = '{}.gz'.format(self.roi_user_space)

        else:
            self.roi_user_space = roi_user_space

        self.verbose = verbose
        self.fsl_laucher = os.path.join(PROJECT_DIR, 'launch_fsl.sh')
        self.afni_laucher = os.path.join(PROJECT_DIR, 'launch_afni.csh')

        self.searchrx = searchrx
        self.searchry = searchry
        self.searchrz = searchrz

        self.clean_intermediate = clean_intermediate

        self.mean_gradient = None

    def clean(self):
        logging.info('deleting intermediate files')

        os.remove(self.matrix_path)
        os.remove(self.rev_matrix_path)
        os.remove(self.roi_user_space)
        os.remove(self.edge_path)

    def fsl_flirt(self, in_file=None, out_file=None, reference=None, out_matrix = None, searchrx=None,
                  searchry=None, searchrz=None, in_matrix=None, applyxfm=None):
        """ Runs FSL flirt with a selected list of options     
        
        :param in_file: 
        :param out_file: 
        :param reference: 
        :return: 
        """

        flirtcmd = [self.fsl_laucher, 'flirt']

        if in_file is not None:
            flirtcmd += ['-in', in_file]
        if out_file is not None:
            flirtcmd += ['-out', out_file]
        if reference is not None:
            flirtcmd += ['-ref', reference]
        if out_matrix is not None:
            flirtcmd += ['-omat', out_matrix]
        if in_matrix is not None:
            flirtcmd += ['-init', in_matrix]
        if searchrx is not None:
            flirtcmd += ['-searchrx', str(searchrx[0]), str(searchrx[1])]
        if searchry is not None:
            flirtcmd += ['-searchry', str(searchry[0]), str(searchry[1])]
        if searchrz is not None:
            flirtcmd += ['-searchrz', str(searchrz[0]), str(searchrz[1])]
        if self.verbose:
            flirtcmd += ['-v']
        if applyxfm is not None:
            flirtcmd += ['-applyxfm']

        logging.debug(' '.join(flirtcmd))
        subprocess.call(flirtcmd)

    def fsl_reverse_xfm(self, in_file=None, out_file=None):
        """ Runs FSL convert xfm with with invert options     

        :param in_file: matrix transform
        :param out_file: inverse matrix transform
        :return: 
    
        convert_xfm -omat <outmat> -inverse <inmat>
            """

        invmat = [self.fsl_laucher, 'convert_xfm', '-omat', out_file, '-inverse', in_file, ]
        logging.debug(' '.join(invmat))
        subprocess.call(invmat)

    def afni_3dedge3(self, in_file=None, out_file=None):
        """Running Afni 3deges3
        
        :param in_file: 
        :param out_file: 
        :param reference: 
        :return: 
        """

        a_3dedge3 = [self.afni_laucher, '3dedge3', '-input', in_file, '-prefix', out_file]

        if self.verbose is not None:
            a_3dedge3.append('-verbose')

        logging.debug(' '.join(a_3dedge3))
        subprocess.call(a_3dedge3)

    def _register(self):
        """Register the image to native space 
        Use the inverse transform matrix to put the mask in user space

        :return: 
        """
        # Registier original image
        logging.info('fsl flirt on {}'.format(self.original_image_path))
        self.fsl_flirt(in_file=self.original_image_path, reference=self.standard_space_image_path,
                       out_file=self.registered_registered_path,
                       out_matrix=self.matrix_path, searchrx=self.searchrx, searchry=self.searchry,
                       searchrz=self.searchrz)
        # Reverse transformation matrix
        logging.info('fsl reverse matrix {}'.format(self.matrix_path))
        self.fsl_reverse_xfm(in_file=self.matrix_path, out_file=self.rev_matrix_path)
        # Deform the roi to original image space
        logging.info('fsl flirt on {}'.format(self.roi_standard_space))
        self.fsl_flirt(in_file=self.roi_standard_space, out_file=self.roi_user_space, in_matrix=self.rev_matrix_path,
                       applyxfm=True, reference=self.original_image_path)

    def binarize(self, image_path, threshold=.3):
        """ Make a 0 1 mask 1 is above a threshold, modify the file in place
        
        :param image_path: math to an image
        :param threshold: Fraction of image.max value
        :return: 
        """

        image = nibabel.load(image_path)
        data = image.get_data()
        new_data = (data > threshold*data.max()).astype(int)
        new_image = nibabel.Nifti2Image(new_data, image.affine)
        new_image.to_filename(image_path)


    def _edges(self):
        """
        Use AFNI's 3Dedge3D to determine the edges of the image
        :return: 
        """
        logging.info('get edges on {}'.format(self.registered_registered_path))
        self.afni_3dedge3(in_file=self.original_image_path, out_file=self.edge_path)
        self.binarize(self.edge_path)

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

        if self.clean_intermediate:
            self.clean()

        return self.mean_gradient


def main(args=None):

    FORMAT = "%(levelname)7s --%(lineno)5s %(funcName)25s():  %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=FORMAT, stream=sys.stdout)

    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(description='QA gradient measures the mean of gradient '
                                                 'of signal in a regions on the back of the head')

    parser.add_argument("--inputs", "-i", type=str, required=True,
                        help='A nifti file or a directory including nifti files')

    parser.add_argument("--output", "-o", type=str, default=None,
                        help='A directory where derivative files are saved')

    parser.add_argument("--clean", type=bool, default=False,
                        help='A directory where derivative files are saved')


    parsed = parser.parse_args(args)

    inputs = parsed.inputs
    output = parsed.output
    clean = parsed.clean

    all_qa = []
    if os.path.isfile(inputs):
        all_qa.append(QaGradient(inputs, output_dir=output, clean_intermediate=clean))
    elif os.path.dirname(inputs):
        all_file = [nii for nii in os.listdir(inputs) if nii.endswith(".nii.gz") or nii.endswith(".nii")]
        for f in all_file:
            all_qa.append(QaGradient(os.path.join(inputs, f), output_dir=output, clean_intermediate=clean))

    for qa in all_qa:
        qa.run()

if __name__ == '__main__':
    main()
