# cubemaker fot rmfit
# sebastian knuettel 26-11-2015
# modified from code made by colm coughlan

#please have Q and U maps in casa format with correct naming convention
#eg	5c4.114_Q1.image
# 	where the stem = '5c4.114_'
#	file ending = '.image'
#	Q1 indicates the first Q image (ascending or descending frequency)
#	same convention is used for Q images
#
#	May add FITS integration for files from aips later

import shutil
import os
import numpy as np
from casa import table as tb

print 'This script will make RM cubes for CASA files \n\n'
#inputs
stem = raw_input('Enter the file stem >> ')
ending = raw_input('Enter the file ending >> ')
#nmaps = 1
nfreqinp = input('Enter the number of frequencies >> ')
nfreq = int(nfreqinp)



#testing below
#image_info = imhead(imagename=stem+'Q2'+ending,mode='list')

#dimx = image_info['shape'][0]
#dimy = image_info['shape'][1]
#
#for k in image_info:
#	if image_info[k] == 'Frequency':
#		freq_axis = int(k[-1])
#	if image_info[k] == 'Stokes':
#		stokes_axis = int(k[-1])

#Here the stokes and frequency axes are found from the second image
#this ensures at least 2 freqiencies are used if file cannot be opened program crashes
ia.open(str(stem+"Q2"+ending))

csys = ia.coordsys()  
ia.done()  
try:  
    	stokes_axis_number = csys.findaxisbyname("stokes", True)  
except Exception:
	print "Stokes axis not found"

try:  
	freq_axis_number = csys.findaxisbyname("frequency", True)  
except Exception:
    	print "Frequency axis not found"  


freq_cube_string=''
for f in range(nfreq):	# For each frequency, make a cube of the Q and U maps
	tstring = stem+'Q'+str(f+1)+ending + ' ' +stem+'U'+str(f+1)+ending
	ostring = stem+str(f)+'.qu.cube.image'
	freq_cube_string = freq_cube_string + ostring+' '
	cube = ia.imageconcat(outfile= ostring, infiles=tstring,axis=stokes_axis_number) # make cube using the Stokes axis
	cube.done()
ostring = stem +'.preRMcube.image'

cube = ia.imageconcat(outfile= ostring, infiles=freq_cube_string,axis=freq_axis_number, relax=T) # now make another cube using the frequency axis - remember to relax other conditions
cube.done()
	#rmfit(imagename=ostring, rm=rmstem+str(i+1)+'.rm.image', rmerr=rmstem+str(i+1)+'.rmerr.image', pa0=rmstem+str(i+1)+'.pa0.image', pa0err=rmstem+str(i+1)+'.pa0err.image')
os.system('rm -rf '+stem+'*.qu.cube*')#removes intermediary cubes







