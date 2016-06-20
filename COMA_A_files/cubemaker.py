
import os


file_stem='Coma_A_Sband_spw'
file_end='_smooth.image'

Cube_name='Coma_A_Sband_'


#Separate out each stokes
for i in range(16,32):

	filename = file_stem+str(i)+file_end
	imsubimage(imagename=filename, outfile=file_stem+str(i)+'_I.temp.im' ,stokes='I')
	imsubimage(imagename=filename, outfile=file_stem+str(i)+'_Q.temp.im', stokes='Q')
	imsubimage(imagename=filename, outfile=file_stem+str(i)+'_U.temp.im', stokes='U')
	
	
#Now make the cubes

cube = ia.imageconcat(outfile=Cube_name+'I.cube.image' , infiles='*_I.temp.im', relax=T) # now make another cube using the frequency axis - remember to relax other conditions
cube.done()
	
cube = ia.imageconcat(outfile=Cube_name+'Q.cube.image' , infiles='*_Q.temp.im', relax=T) # now make another cube using the frequency axis - remember to relax other conditions
cube.done()

cube = ia.imageconcat(outfile=Cube_name+'U.cube.image' , infiles='*_U.temp.im', relax=T) # now make another cube using the frequency axis - remember to relax other conditions
cube.done()

os.system('rm -rf *.temp.im') #removes the intermediate images