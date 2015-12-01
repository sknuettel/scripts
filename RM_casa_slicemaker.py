# Sebastian Knuettel 01-12-2015
# This is code for generating 1D slices from RM images in casa
# data is saved as .csv and a quick plot is made to visualise the slice
#
#
#
#
#
#
#

#import shutil
#import os
import numpy as np
import matplotlib.pyplot as plt
#from casa import table as tb


RM_stem = raw_input('Please enter RM image name stem >>')

blcx = input('BLC X >>')
blcy = input('BLC Y >>')
trcx = input('TRC X >>')
trcy = input('TRC Y >>')

N_PTS = 250


#single line slice
ia.open(RM_stem+'.rm.image')
rec = ia.getslice( x=[blcx,trcx],y=[blcy,trcy],npts=N_PTS,method = 'linear' )
RM_vals = rec['pixel']
D_vals = rec['distance']
ia.close()

ia.open(RM_stem+'.rmerr.image')
rec = ia.getslice( x=[blcx,trcx],y=[blcy,trcy],npts=N_PTS,method = 'linear' )
RM_err_vals = rec['pixel']
ia.close()


#get cellsize from image in radians
cellsize = (imhead(imagename=RM_stem+'.rm.image',mode='get',hdkey='cdelt2'))['value']

cellsize = abs(cellsize)
cellsize = cellsize*206264.8062 #converts to arcsec

D_vals =  np.multiply(D_vals,cellsize) #converts pixel distance to arcsec



outslice = np.column_stack((D_vals,RM_vals,RM_err_vals)) #creates 2d array for output


print 'Slice read successfully!!!\n\n'
outname = raw_input('Please input name stem for slice file >>')

np.savetxt(outname+'.csv', outslice, fmt = '%1.4e', delimiter = ',',header= 'Distance(arcsec),RM(rad/m/m),RMerr(rad/m/m)')

#calculates significance of slice
sigma = np.abs(RM_vals[0] - RM_vals[-1])
sigma = sigma/(np.sqrt(RM_err_vals[0]*RM_err_vals[0] + RM_err_vals[-1]*RM_err_vals[-1]))
sigma = round(sigma,1)

plt.figure(figsize=(10,6))
plt.plot(D_vals, RM_vals, 'k-', linewidth = 3) #plots slice
plt.fill_between(D_vals, RM_vals-RM_err_vals, RM_vals+RM_err_vals, facecolor ='gray') #plots error bars
#the following changes font sizes for the labels
plt.xlabel('Transverse Slice (arcsec)', fontsize=20)
plt.xlim(xmin=-cellsize)
plt.xticks(fontsize = 16)
plt.yticks(fontsize = 16)
plt.ylabel('Rotation Measure (rad m$^{-2}$)',fontsize=20)
plt.title(r'Significance  %.1f$\sigma$' % sigma, fontsize=18, ) #Notice the r before the string

print 'Done!!!\n'


