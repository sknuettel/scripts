import numpy as np
import shutil
import os
from casa import table as tb



#function to create an accurate noise map including dterm noise mentioned by hovatta
def calc_tot_noise(ICL_filename = "",QorU_filename="",noise_outfile="",Nant='',Nif='',Nsc='',Noise_box=''):

	dval = 0.000004/(Nant*Nif*Nsc)
	Imax  = imhead(ICL_filename,mode='get',hdkey='datamax')#gets max I
	Imax_term = 0.09*(Imax*Imax)
	
	
	boxstat = imstat(imagename=QorU_filename,box = str(Noise_box[0])+','+str(Noise_box[1])+ \
	','+str(Noise_box[2])+','+str(Noise_box[3])) #image statistics for noise box
	
	rms_noise = boxstat['rms'][0] #retrieves rms 
	rms_val = 3.25*rms_noise*rms_noise #gets (1.8*rms)^2


	formula = 'sqrt( '+str(rms_val)+' + '+str(dval)+'*(IM0*IM0 + '+str(Imax_term)+') )'#equation for immath
	immath(imagename=ICL_filename,mode= 'evalexpr',expr=formula,outfile=noise_outfile) #immath call
	
	return()

#Noisebox = [blcx, blcy, trcx, trcy]
#calc_tot_noise('0923_int_I1.CLEAN.image', '0923_int_Q1.CLEAN.image', '0923_Q1_noise_test.im', 10, 1,8, [27,21,235,83] )

print 'This script will make accurate noise maps for CASA files \n\n'
#inputs
stem = raw_input('Enter the file stem >> ')
ending = raw_input('Enter the file ending >> ')
#nmaps = 1
nfreqinp = input('Enter the number of frequencies >> ')
nfreq = int(nfreqinp)

Nif = []
for f in range(nfreq):

	Nif_in = input('Enter number of IF\'s in frequency '+str(f+1)+' >> ')
	Nif.append(Nif_in)


Nant = input('Enter number of antennae >> ')
Nsc = input('Enter number of scans >> ')


blcx = input('Enter the blc x of noise box >> ')
blcy = input('Enter the blc y of noise box >> ')
trcx = input('Enter the trc x of noise box >> ')
trcy = input('Enter the trc y of noise box >> ')

Noisebox = [blcx, blcy, trcx, trcy]

for f in range(nfreq):

	istring = stem+'I'+str(f+1)+ending
	qstring = stem+'Q'+str(f+1)+ending
	ustring = stem+'U'+str(f+1)+ending #filenames

	calc_tot_noise(istring,qstring,stem+'Q'+str(f+1)+'_noise.image',Nant,Nif[f],Nsc,Noisebox)
	calc_tot_noise(istring,ustring,stem+'U'+str(f+1)+'_noise.image',Nant,Nif[f],Nsc,Noisebox)

#writes as FITS for AIPS use
	exportfits(stem+'Q'+str(f+1)+'_noise.image',stem+'Q'+str(f)+'_noise.FITS')
	exportfits(stem+'U'+str(f+1)+'_noise.image',stem+'U'+str(f)+'_noise.FITS')



	









