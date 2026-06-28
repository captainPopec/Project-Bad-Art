import maad
from maad import sound, rois, spl, features, util
import maad.features
import numpy as np
import matplotlib.pyplot as plt 


#s, fs = sound.load('C:/Users/Korisnik/OneDrive - Prirodoslovno-matematički fakultet/Self Investing/Projekti/Bad Art/pjesme/Fanfare and prologue.wav')
#s, fs = sound.load('C:/Users/Korisnik/OneDrive - Prirodoslovno-matematički fakultet/Self Investing/Projekti/Bad Art/Podatci za analizu/Antropofonija/Spectre.wav')
s, fs = sound.load('C:/Users/Korisnik/Downloads/Spectre[1].wav')
#rois.find_rois_cwt(s, fs, flims=(4500,8000), tlen=2, th=0, display=True)


Sxx, tn, fn, ext=sound.spectrogram(s, fs, mode='amplitude')   #treba paziti koji tip spektrograma se radi, amplitudni ili frekvencijski?

Sxx_power, tn, fn, ext=sound.spectrogram(s, fs)   
Sxx_dB = util.power2dB(Sxx_power) +96   

Sxx_dB_noNoise, noise_profile, c = sound.remove_background(Sxx_dB)

#med=features.temporal_median(s)
#print(med)

#ari=features.acoustic_richness_index([tEntropy],[med])  #za oba audia vraća 1, zar su prekratki mozda ili neke pstavek ne valjaju? - probaj  seawave
#print(ari)

#fract, count, mean= features.temporal_activity(s,6)     #Jako KORISNO - mean varijabla kaze koliko je prosjek dB signala iznad tresholda - default = 3 ali mogu ga zadat kao drugi argumetn funkcije
#print(fract,'', count,'', mean)

#a ,b , ACI = features.acoustic_complexity_index(Sxx)    #zahtijeva amplitudni spektrogram
#print(ACI)


'''
entropy - najdraži dio
Cijeli svemir teži mirovannju, to čini jednolikim raspodijelom energije, 

--> dakle H ~ raspodijela jednolikija <--

zato će Hf biti velika ako je jednaka količina energije signala raspoređena po svim frekvencijama, no ako je mala entropija znači da su samo neke frekvencije zastupljene
Dakle ako je puno signala koje mozak mora obraditi očekujem malu entropiju - zannimljivo je da je i čovječji zvuk niske entropije
'''

#Hf, Ht_per_bin= features.frequency_entropy(Sxx_dB_noNoise)
#print(Hf)

#tEntropy=features.temporal_entropy(s)
#print(tEntropy)

#EAS, ECU, ECV, EPS, EPS_KURT, EPS_SKEW = features.spectral_entropy(Sxx_power, fn) 
#print('EAS: %2.2f / ECU: %2.2f / ECV: %2.2f / EPS: %2.2f / EPS_KURT: %2.2f / EPS_SKEW: %2.2f' % (EAS, ECU, ECV, EPS, EPS_KURT, EPS_SKEW))

#ACTspfract_per_bin, ACTspcount_per_bin, ACTspmean_per_bin = features.spectral_activity(Sxx_dB_noNoise)  
#print('Mean proportion of spectrogram above threshold : %2.2f%%' %np.mean(ACTspfract_per_bin)) 

#LFC, MFC, HFC = features.spectral_cover(Sxx_dB_noNoise, fn) 
#print('LFC: %2.2f / MFC: %2.2f / HFC: %2.2f' % (LFC, MFC, HFC)) 

#NDSI, ratioBA, antroPh, bioPh  = features.soundscape_index(Sxx_power,fn)
#print('NDSI Soundecology : %2.2f ' %NDSI) 
#NDSI, ratioBA, antroPh, bioPh  = features.soundscape_index(Sxx_dB_noNoise,fn,R_compatible=None)
#print('NDSI MAAD: %2.2f ' %NDSI) 

#BI  = features.bioacoustics_index(Sxx,fn,R_compatible=None)
#print('BI MAAD : %2.2f ' %BI) 

a1,a2,tS2N = maad.sound.temporal_snr(s)
print(tS2N)

'''
s, fs= maad.sound.load('C:/Users/Korisnik/OneDrive - Prirodoslovno-matematički fakultet/Self Investing/Projekti/Bad Art/pjesme/Fanfare and prologue.wav', detrend=False)
Sxx, tn, fn, ext = maad.sound.spectrogram (s, fs, nperseg=int(fs/10), noverlap=0, mode='amplitude', detrend=False)  
ADI  = maad.features.acoustic_diversity_index(Sxx,fn,fmax=20000)
print('ADI : %2.2f ' %ADI) 
   
AEI  = maad.features.acoustic_eveness_index(Sxx,fn,fmax=20000)
print('AEI : %2.2f '%AEI)
'''




#############


