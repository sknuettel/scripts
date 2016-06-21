#This script attempts to automate the calibration process done for Coma A EVLA data
#can be applied to other observations if modified slightly

import re
import os


#polarization calibration needs to be fixed to be more general
#SETTING VARIABLES, FILENAMES, AND PARAMETERS
##########################################################################################


visname = 'Coma_A_Sband-hanning.ms' #put the name for uncalibrated visibility ms here

splitname = 'Coma_A_vis_split_script.ms'#name for desired calibrated split data of source

table_nam = 'Coma_A_vis_script' #name stem for the calibration tables applied and plots made

antref = 'ea10' #central reference antenna

bpcal = '3C 286' #bandpass calibrator

phascal = '3C286P' #name of phase calibrator

fluxcal = '3C 286' #name of flux calibrator
model_nam = '3C286_S.im' #model file to use


source = 'COMA A' #source name

spw_select = '16~31' #spw selection all channels

spw_centralchans = '16~31:28~36'  #spws and their central channels for initial phase cal

spw_noedges = '16~31:5~58' #ignoring edge channels with lower sensitivity

doplot = False





#ANTENNA POSN CORRECTION
##########################################################################################


os.system('rm -rf '+table_nam+'.antpos') #removes all old tables 
#create antenna position table to correct for antenna positions in later steps
gencal(vis=visname,caltable= table_nam +'.antpos',caltype='antpos')


##########################################################################################





#SET FLUX SCALE TO FLUX CALIBRATOR USING MODEL
##########################################################################################

#lists models
setjy(vis=visname,listmodels=T)


#set flux scale for the flux calibrator using a model
fluxdata = setjy(vis=visname,field=fluxcal,standard='Perley-Butler 2013',
	model=model_nam,usescratch=False,scalebychan=True,spw=spw_select)
	
	
##########################################################################################


	
	
#DO AN INITIAL PHASE CALIBRATION WHICH WILL BE USED FOR THE BANDPASS AND DELAY
##########################################################################################

os.system('rm -rf '+table_nam+'.G0all') #removes all old tables 

gaincal(vis=visname, caltable=table_nam + '.G0all',
field = fluxcal+','+phascal+','+bpcal, refant=antref,spw= spw_centralchans ,gaintype='G',
calmode='p',solint='int', minsnr=5.0, gaintable=[table_nam+'.antpos'])

#uses central channels for high snr

if doplot:
	plotcal(caltable=table_nam+'.G0all',xaxis='time',yaxis='phase',
        poln='R',iteration='antenna',plotrange=[-1,-1,-180,180])



##########################################################################################



	

#DELAY CALIBRATION FOR ANTENNA BASED DELAY
##########################################################################################


os.system('rm -rf '+table_nam+'.K0') #removes all old tables 

gaincal(vis=visname, caltable= table_nam + '.K0', field=bpcal, refant = antref,
	spw=spw_noedges, gaintype = 'K', solint = 'inf',combine='scan',minsnr=5.0,
	gaintable=[table_nam+'.G0all',table_nam+'.antpos'])
	
if doplot:
	plotcal(caltable=table_nam+'.K0',xaxis='antenna',yaxis='delay',
        figfile='plotcal_'+table_nam+'-K0-delay.png')

##########################################################################################


	
	
#BANDPASS CALIBRATION
##########################################################################################
	
	
os.system('rm -rf '+table_nam+'.B0') #removes all old tables 

bandpass(vis=visname, caltable=table_nam+'.B0', field = bpcal,
	spw=spw_select, refant=antref, combine ='scan', solint ='inf', bandtype='B',
	gaintable=[table_nam+'.antpos',table_nam+'.G0all',table_nam+'.K0'])

if doplot:
	plotcal(caltable= table_nam+'.B0',poln='R', 
        xaxis='chan',yaxis='amp',field= bpcal,subplot=221, 
        iteration='antenna',figfile='plotcal_'+table_nam+'-B0-R-amp.png')

	plotcal(caltable= table_nam+'.B0',poln='L', 
        xaxis='chan',yaxis='amp',field= bpcal,subplot=221, 
        iteration='antenna',figfile='plotcal_'+table_nam+'-B0-L-amp.png')
#
	plotcal(caltable= table_nam+'.B0',poln='R', 
        xaxis='chan',yaxis='phase',field= bpcal,subplot=221, 
        iteration='antenna',plotrange=[-1,-1,-180,180],
        figfile='plotcal_'+table_nam+'-B0-R-phase.png')
#
	plotcal(caltable= table_nam+'.B0',poln='L', 
        xaxis='chan',yaxis='phase',field= bpcal,subplot=221, 
        iteration='antenna',plotrange=[-1,-1,-180,180],
        figfile='plotcal_'+table_nam+'-B0-L-phase.png')




##########################################################################################

	
#GAIN CALIBRATION
##########################################################################################

#for flux calibrator

os.system('rm -rf '+table_nam+'.G1') #removes all old tables 
gaincal(vis=visname,caltable=table_nam+'.G1', field = fluxcal, spw= spw_noedges,
	solint ='inf',refant=antref, gaintype = 'G', calmode = 'ap', solnorm = F,
	gaintable=[table_nam+'.antpos',
        table_nam+'.K0',
        table_nam+'.B0'],
	interp=['linear','linear','nearest'])


#for phase calibrator	
gaincal(vis=visname,caltable=table_nam+'.G1', field = phascal, spw= spw_noedges,
	solint ='inf',refant=antref, gaintype = 'G', calmode = 'ap',
	gaintable=[table_nam+'.antpos',
        table_nam+'.K0',
        table_nam+'.B0'],
	append=T)

##########################################################################################


#POLARIZATION CALIBRATION (UNDER CONSTRUCTION)
##########################################################################################


#creating polarized fluxcal model with setjy

#the below has to be fixed to be more general but it works for the coma a data in s band
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#have to find way to read Ipb[] and freq[] from the visibility or using setjy 

#(ms.getspectralwindowinfo might have the function i seek)


#calculated perley butler I fluxes for above freqs (can get this from setjy)
Ipb=[12.581,12.15,11.754,11.387,11.046,10.729,10.432,10.154,9.9412,9.6929,9.4588,9.2376,9.0282,8.8297,8.6411,8.4617]

#freqs from beginning of every spw
freq=[1.988,2.116,2.244,2.372,2.500,2.628,2.756,2.884,2.988,3.116,3.244,3.372,3.500,3.628,3.756,3.884]

d0=33*pi/180 #pol angle in rads for 3C286
alpha =0.0 #setting spix
for i in range(0,16):
	
	print i
	j=int(i)
	freqstr = str(freq[j])+'GHz'
	Fpol = -0.067*pow(freq[j],2.0) +0.958*freq[j] + 8.514 #specific to S band range
	Fpol = Fpol/100.0
	if freq[j] < freq[-1]:
		alpha = log(Ipb[int(j+1)]/Ipb[j])/log(freq[j+1]/freq[j])#calculating spix
	
	
	#if at last spw we use the previous alpha	
	setjy(vis=visname,field=fluxcal, standard= 'manual', spw=str(j+16),
		fluxdensity=[Ipb[j],0,0,0],spix=[alpha,0],reffreq=freqstr,selectdata=T
		,polindex=[Fpol,0],polangle=[d0,0], scalebychan=T,usescratch=F)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


os.system('rm -rf '+table_nam+'.Kcross') #removes all old tables 
#solving for cross hand delays
gaincal(vis=visname, caltable =table_nam+'.Kcross',
	field = fluxcal, spw=spw_noedges,gaintype='KCROSS',
	solint='inf',combine='scan',refant=antref,
	gaintable=[table_nam+'.antpos',
		table_nam+'.K0',
		table_nam+'.B0',
		table_nam+'.G1'],
	gainfield=['','','',fluxcal],
	parang=T)

if doplot:
	plotcal(caltable=table_nam+'.Kcross', yaxis='delay', xaxis='antenna',iteration='spw')

os.system('rm -rf '+table_nam+'.D1') #removes all old tables 
#Solving for the Leakage Terms
polcal(vis=visname, caltable=table_nam+'.D1',
	field=phascal, spw=spw_select,refant=antref, poltype='Df+QU', solint='inf',combine='scan',
	gaintable=[table_nam+'.antpos',
		table_nam+'.K0',
		table_nam+'.B0',
		table_nam+'.G1',
		table_nam+'.Kcross'],
	gainfield=['','','',phascal,''])

#note that full width of spw's was used as we have a bandpass table to apply


os.system('rm -rf '+table_nam+'.X1') #removes all old tables 
#solving R-L polarization angle:
polcal(vis=visname, caltable=table_nam+'.X1',
	field=fluxcal, combine ='scan',poltype='Xf',solint ='inf',
	gaintable=[table_nam+'.antpos',
		table_nam+'.K0',
		table_nam+'.B0',
		table_nam+'.G1',
		table_nam+'.Kcross',
		table_nam+'.D1'],
	gainfield=['','','',fluxcal,'',''])


##########################################################################################



#APPLYING THE CALIBRATION
##########################################################################################

#apply calibration to calibrators
applycal(vis=visname,field=fluxcal,
	gaintable=[table_nam+'.antpos',
		table_nam+'.G1',
		table_nam+'.K0',
		table_nam+'.B0',
		table_nam+'.Kcross',
		table_nam+'.D1',
		table_nam+'.X1'],
	gainfield=['',fluxcal,'','','','',''],
	interp=['','nearest','','','','',''],
	calwt=[False],
	parang=True)

applycal(vis=visname,field=phascal,
	gaintable=[table_nam+'.antpos',
		table_nam+'.G1',
		table_nam+'.K0',
		table_nam+'.B0',
		table_nam+'.Kcross',
		table_nam+'.D1',
		table_nam+'.X1'],
	gainfield=['',phascal,'','','','',''],
	interp=['','nearest','','','','',''],
	calwt=[False],
	parang=True)



#apply calibration to source
applycal(vis=visname,field=source,
	gaintable=[table_nam+'.antpos',
		table_nam+'.G1',
		table_nam+'.K0',
		table_nam+'.B0',
		table_nam+'.Kcross',
		table_nam+'.D1',
		table_nam+'.X1'],
	gainfield=['',phascal,'','','','',''],
	interp=['','linear','','','','',''],
	calwt=[False],
	parang=True)
	
if doplot:
	plotms(vis=visname,xaxis='amp',yaxis='uvdist',field=phascal)

##########################################################################################


confirm = input('Do you want to split off the source data? [1/0] >>')

#SPLITTING OFF THE SOURCE DATA
##########################################################################################
if confirm:

	split(vis=visname,outputvis=splitname,
		datacolumn='corrected',field=source)

##########################################################################################























