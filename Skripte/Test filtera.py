import maad
import maad.sound
import numpy as np
import matplotlib.pyplot as plt 


s, fs = maad.sound.load('C:/Users/Korisnik/OneDrive - Prirodoslovno-matematički fakultet/Self Investing/Projekti/Bad Art/Podatci za analizu/Antropofonija/Spectre.wav')
#s, fs= maad.sound.load('C:/Users/Korisnik/OneDrive - Prirodoslovno-matematički fakultet/Self Investing/Projekti/Bad Art/Podatci za analizu/rock_savanna.wav') 



#Sxx, tn, fn, ext=sound.spectrogram(s, fs, mode='amplitude')   #treba paziti koji tip spektrograma se radi, amplitudni ili frekvencijski?




#Background remove  ---najpouzadniji
Sxx_power, tn, fn, ext=maad.sound.spectrogram(s, fs)  
Sxx_dB = maad.util.power2dB(Sxx_power) +96   
#Sxx_dB_noNoise, noise_profile, c= maad.sound.remove_background(Sxx_dB)
Sxx_dB_noNoise,_,_ = maad.sound.remove_background_morpho(Sxx_dB, q=0.95)
#Sxx_noNoise = maad.sound.median_equalizer(Sxx_power, display=True, extent=ext)
#Sxx_dB_noNoise = maad.util.power2dB(Sxx_noNoise) 
 
fig, (ax1, ax2) = plt.subplots(2, 1)
maad.util.plot2d(Sxx_dB, ax=ax1, extent=ext, title='original', vmin=np.median(Sxx_dB), vmax=np.median(Sxx_dB)+40)
maad.util.plot2d(Sxx_dB_noNoise, ax=ax2, extent=ext, title='Without stationary noise', vmin=np.median(Sxx_dB_noNoise), vmax=np.median(Sxx_dB_noNoise)+40)
fig.set_size_inches(15,8)
fig.tight_layout()




'''
#remove background morpho math tool -najbolji je 0.6
Sxx,tn,fn,ext = maad.sound.spectrogram (s, fs)
Sxx_dB = maad.util.power2dB(Sxx) +96
Sxx_dB_noNoise_q25,_,_ = maad.sound.remove_background_morpho(Sxx_dB, q=0.85)
Sxx_dB_noNoise_q50,_,_ = maad.sound.remove_background_morpho(Sxx_dB, q=0.90)
Sxx_dB_noNoise_q75,_,_ = maad.sound.remove_background_morpho(Sxx_dB, q=0.97)
fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
maad.util.plot2d(Sxx_dB_noNoise_q25, ax=ax1, extent=ext, title='Without stationary noise (q=0.25)',vmin=np.median(Sxx_dB_noNoise_q25), vmax=np.median(Sxx_dB_noNoise_q25)+40)
maad.util.plot2d(Sxx_dB_noNoise_q50, ax=ax2, extent=ext, title='Without stationary noise (q=0.50)',vmin=np.median(Sxx_dB_noNoise_q50), vmax=np.median(Sxx_dB_noNoise_q50)+40)
maad.util.plot2d(Sxx_dB_noNoise_q75, ax=ax3, extent=ext, title='Without stationary noise (q=0.75)',vmin=np.median(Sxx_dB_noNoise_q75), vmax=np.median(Sxx_dB_noNoise_q75)+40)
fig.set_size_inches(15,9)
fig.tight_layout()    




#along axis  -- previše ga ostruže
Sxx,tn,fn,ext = maad.sound.spectrogram (s, fs)   
Sxx_dB = maad.util.power2dB(Sxx) + 96
Sxx_dB_noNoise_ale,_ = maad.sound.remove_background_along_axis(Sxx_dB, mode='ale')    
Sxx_dB_noNoise_med,_ = maad.sound.remove_background_along_axis(Sxx_dB, mode='median')
Sxx_dB_noNoise_mean,_ = maad.sound.remove_background_along_axis(Sxx_dB, mode='mean')
fig, (ax2, ax3, ax4) = plt.subplots(3, 1)
#maad.util.plot2d(Sxx_dB, ax=ax1, extent=ext, title='original', vmin=np.median(Sxx_dB), vmax=np.median(Sxx_dB)+40)
maad.util.plot2d(Sxx_dB_noNoise_ale, ax=ax2, extent=ext, title='Without stationary noise (mode = ''ale'')',vmin=np.median(Sxx_dB_noNoise_ale), vmax=np.median(Sxx_dB_noNoise_ale)+40)
maad.util.plot2d(Sxx_dB_noNoise_med, ax=ax3, extent=ext, title='Without stationary noise (mode = ''med'')',vmin=np.median(Sxx_dB_noNoise_med), vmax=np.median(Sxx_dB_noNoise_med)+40)
maad.util.plot2d(Sxx_dB_noNoise_mean, ax=ax4, extent=ext, title='Without stationary noise (mode = ''mean'')',vmin=np.median(Sxx_dB_noNoise_mean), vmax=np.median(Sxx_dB_noNoise_mean)+40)
fig.set_size_inches(8,10)
fig.tight_layout()
'''




plt.show()