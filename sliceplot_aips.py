
# The following python script is designed to plot 
# the typical RM slices created in AIPS using the
# task 'SLICE'. The slice files are txt files which
# are imported by this scipt and plotted and exported 
# as .png files. The plotted data is also exported
# as a csv file.
#
#
# Sebastian Knuettel 21/09/2015
#


import matplotlib.pyplot as plt
import numpy as np




filename_RM = raw_input("Please enter the filename for the RM slice. >>")

filename_Err = raw_input("Now please enter the filename for the RM error slice. >>")

cellsize = input("Please enter the cellsize in mas. >>")

#reads the files
dx,dy,RM = np.loadtxt( filename_RM, skiprows=1, unpack=True, usecols = (0,1,2))
dx2, RMerr = np.loadtxt( filename_Err, skiprows=1, unpack=True, usecols =(0, 2))

dx = dx - dx[0]
dy = dy - dy[0]

dmas = np.sqrt(dx*dx +dy*dy)
dmas = dmas*cellsize


#calculates sigma
sigma = np.abs(RM[0] - RM[-1])
sigma = sigma/(np.sqrt(RMerr[0]*RMerr[0] + RMerr[-1]*RMerr[-1]))
sigma = round(sigma,1)

plotname = raw_input("Please enter desired name of the plotfile. >>")

plt.figure(figsize=(10,6))
plt.plot(dmas, RM, 'k-', linewidth = 3) #plots slice
plt.fill_between(dmas, RM-RMerr, RM+RMerr, facecolor ='gray') #plots error bars
#the following changes font sizes for the labels
plt.xlabel('Transverse Slice (mas)', fontsize=20)
plt.xlim(xmin=-0.1)
plt.xticks(fontsize = 16)
plt.yticks(fontsize = 16)
plt.ylabel('Rotation Measure (rad m$^{-2}$)',fontsize=20)
plt.title(r'Significance  %.1f$\sigma$' % sigma, fontsize=18, ) #Notice the r before the string
#xmin, xmax = xlim()
#ymin, ymax = ylim()   # return the current xlim
#plt.text(0.5*(xmax - xmin),0.8*ymax,r'Significance  %.1f$\sigma$' % sigma,fontsize=16)

plt.savefig(''+ plotname + '.png')

outfile = np.column_stack((dmas, RM, RMerr)) #puts data for writout in 2d array


np.savetxt(plotname + '_slicedata.csv', outfile, fmt = '%1.4e', delimiter = ',', header='Distance(mas),RM(rad/m^2),RMerror(rad/m^2)')#saves data as csv if user needs it later

print 'The plot data has been written to '+ plotname +'_slicedata.csv for your \n convenience'






