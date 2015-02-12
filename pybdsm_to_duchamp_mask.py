# PyBDSM starts counting islands at zero, while Duchamp starts at 1. Flagged regions =-1 in PyBDSM, 0 in Duchamp
# (Using PyBDSM process_image task)
# This script just adds one to the entire PyBDSM map, converting it to a Duchamp-style map
# Colm Coughlan
# 12.2.15

import sys
import numpy as np
import pyfits

# Check arguments

if(len(sys.argv)!=2):
	print("\tError: Takes one argument.")
	print("\tUseage: pybdsm_to_duchamp_mask <filename>")
	sys.exit()
else:
	inputname = str(sys.argv[1])
	print('\tConverting '+inputname+' to Duchamp format.')

# Open fits file and add one to data area
# Update existing file and close it

f = pyfits.open(inputname,mode='update')
f[0].data = np.add(f[0].data,1)
f.flush()
f.close()

print('\tProcess complete.')
