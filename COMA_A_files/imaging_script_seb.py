


File_stem='Coma_A_Sband_spw'

visname = 'Coma_A_Sband_split1.ms'



for i in range(0,15):
	
	tclean(vis=visname, field='COMA A', spw= str(i+17),cell=['0.15arcsec'],
		imagename = File_stem + str(i+17),
		datacolumn = 'corrected', imsize = [1024,1024],stokes = 'IQUV',specmode='mfs',
		deconvolver='multiscale', scales =[0,6,20,60],smallscalebias=0.7,
		weighting='briggs',robust=0.5, uvtaper = ['70klambda','80klambda'],niter = 20000,
		threshold='0.25mJy',cyclefactor = 1.5,interactive=F,usemask='user',
		mask=['Coma_A_Sband_spw1_5.mask'],restart=F,savemodel='none')
	
	
	
