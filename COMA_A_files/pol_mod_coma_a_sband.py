
#freqs from beginning of every spw
Ipb=[12.581,12.15,11.754,11.387,11.046,10.729,10.432,10.154,9.9412,9.6929,9.4588,9.2376,9.0282,8.8297,8.6411,8.4617]


#calculated perley butler I fluxes for above freqs
freq=[1.988,2.116,2.244,2.372,2.500,2.628,2.756,2.884,2.988,3.116,3.244,3.372,3.500,3.628,3.756,3.884]

d0=33*pi/180 #pol angle in rads for 3C286
alpha =0.0 #setting spix
for i in range(0,16):
	
	print i
	j=int(i)
	freqstr = str(freq[j])+'GHz'
	Fpol = -0.067*pow(freq[j],2.0) +0.958*freq[j] + 8.514
	Fpol = Fpol/100.0
	if freq[j] < freq[-1]:
		alpha = log(Ipb[int(j+1)]/Ipb[j])/log(freq[j+1]/freq[j])#calculating spix
	
	
	#if at last spw we use the previous alpha	
	setjy(vis=sbandvis,field='3C 286', standard= 'manual', spw=str(j+16),
fluxdensity=[Ipb[j],0,0,0],spix=[alpha,0],reffreq=freqstr,scan='3,4',selectdata=T
,polindex=[Fpol,0],polangle=[d0,0], scalebychan=T,usescratch=F)
	
	
	
		
	