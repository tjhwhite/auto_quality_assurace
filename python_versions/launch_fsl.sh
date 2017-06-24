#!/usr/bin/env bash
### YOUR FSL PATH and version HERE
FSLDIR=/usr/local/fsl
### Nothing else to do

. $HOME/.config/qagradient/fsl

. ${FSLDIR}/etc/fslconf/fsl.sh
export PATH=${FSLDIR}/bin:${PATH}
export FSLDIR


$*

