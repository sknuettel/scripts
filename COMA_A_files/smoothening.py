bmaj = '3.29913arcsec'
bmin = '3.05511arcsec'
bpa = '76.62319deg'
File_stem='Coma_A_Sband_spw'


for i in range(0,15):


	filenum = File_stem+str(i+17)
	imsmooth( imagename=filenum+'.image',outfile=filenum+'_smooth.image', kernel='gauss', major=bmaj, minor=bmin, pa=bpa,
			targetres = True,)