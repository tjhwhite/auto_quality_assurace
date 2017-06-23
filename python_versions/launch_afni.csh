#!/usr/bin/env tcsh
### YOUR AFNIN BIN PATH HERE
set AFNI_BIN = /home/poquirion/abin

#### NOTHING ELSE TO SET


set path = ( $path  $AFNI_BIN  )
if ( -f $HOME/.afni/help/all_progs.COMP ) then
   source $HOME/.afni/help/all_progs.COMP
endif

#ahdir=`apsearch -afni_help_dir`
#if [ -f "$ahdir/all_progs.COMP.bash" ]
#then
#   . $ahdir/all_progs.COMP.bash
#fi

$*