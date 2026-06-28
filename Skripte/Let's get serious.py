import maad
from maad import sound, rois, spl, features, util
import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd
import time


start_time = time.time()



'''
#antropofinija
s_dinamo, fs_dinamo = sound.load('C:/Users/Korisnik/OneDrive - Prirodoslovno-matematički fakultet/Self Investing/Projekti/Bad Art/Podatci za analizu/Antropofonija/Dinamo quarabag.wav' )
s_dnova, fs_dnova = sound.load('C:/Users/Korisnik/OneDrive - Prirodoslovno-matematički fakultet/Self Investing/Projekti/Bad Art/Podatci za analizu/Antropofonija/Dnevnik nove tv.wav' )
s_fanfare, fs_fanfare = sound.load('C:/Users/Korisnik/OneDrive - Prirodoslovno-matematički fakultet/Self Investing/Projekti/Bad Art/Podatci za analizu/Antropofonija/Fanfare and Prologue.wav' )
s_reklame, fs_reklame = sound.load('C:/Users/Korisnik/OneDrive - Prirodoslovno-matematički fakultet/Self Investing/Projekti/Bad Art/Podatci za analizu/Antropofonija/Reklame.wav' )
s_direkt, fs_direkt = sound.load('C:/Users/Korisnik/OneDrive - Prirodoslovno-matematički fakultet/Self Investing/Projekti/Bad Art/Podatci za analizu/Antropofonija/Rtl direkt.wav' )
s_spidey, fs_spidey = sound.load('C:/Users/Korisnik/OneDrive - Prirodoslovno-matematički fakultet/Self Investing/Projekti/Bad Art/Podatci za analizu/Antropofonija/The Amazing Spider-Man 2 theme song.wav' )
s_jala, fs_jala = sound.load('C:/Users/Korisnik/OneDrive - Prirodoslovno-matematički fakultet/Self Investing/Projekti/Bad Art/Podatci za analizu/Antropofonija/Jala.wav' )
s_jbp, fs_jbp = sound.load('C:/Users/Korisnik/OneDrive - Prirodoslovno-matematički fakultet/Self Investing/Projekti/Bad Art/Podatci za analizu/Antropofonija/JBP.wav' )
s_lasagna, fs_lasagna = sound.load('C:/Users/Korisnik/OneDrive - Prirodoslovno-matematički fakultet/Self Investing/Projekti/Bad Art/Podatci za analizu/Antropofonija/Lasagna.wav' )
s_peki, fs_peki = sound.load('C:/Users/Korisnik/OneDrive - Prirodoslovno-matematički fakultet/Self Investing/Projekti/Bad Art/Podatci za analizu/Antropofonija/Peki.wav' )
s_spectre, fs_spectre = sound.load('C:/Users/Korisnik/OneDrive - Prirodoslovno-matematički fakultet/Self Investing/Projekti/Bad Art/Podatci za analizu/Antropofonija/Spectre.wav' )
s_zzk, fs_zzk = sound.load('C:/Users/Korisnik/OneDrive - Prirodoslovno-matematički fakultet/Self Investing/Projekti/Bad Art/Podatci za analizu/Antropofonija/Žžk_deb.wav')
s_got, fs_got = sound.load('C:/Users/Korisnik/OneDrive - Prirodoslovno-matematički fakultet/Self Investing/Projekti/Bad Art/Podatci za analizu/Antropofonija/GoT.wav')
s_kor, fs_kor = sound.load('C:/Users/Korisnik/OneDrive - Prirodoslovno-matematički fakultet/Self Investing/Projekti/Bad Art/Podatci za analizu/Antropofonija/Korado.wav')
'''
s_vivaldi, fs_vivaldi= sound.load('C:/Users/Korisnik/OneDrive - Prirodoslovno-matematički fakultet/Self Investing/Projekti/Bad Art/Podatci za analizu/Antropofonija/Vivaldi.wav')
s_mozart, fs_mozart = sound.load('C:/Users/Korisnik/OneDrive - Prirodoslovno-matematički fakultet/Self Investing/Projekti/Bad Art/Podatci za analizu/Antropofonija/Lacrimosa.wav')
s_pejacevic, fs_pejacevic = sound.load('C:/Users/Korisnik/OneDrive - Prirodoslovno-matematički fakultet/Self Investing/Projekti/Bad Art/Podatci za analizu/Antropofonija/Pejac.wav')
s_fiori, fs_fiori = sound.load('C:/Users/Korisnik/OneDrive - Prirodoslovno-matematički fakultet/Self Investing/Projekti/Bad Art/Podatci za analizu/Antropofonija/Tchaikovsky.wav')

'''
#Biofonija
s_nocfor_Gab, fs_nocfor_Gab = sound.load('C:/Users/Korisnik/OneDrive - Prirodoslovno-matematički fakultet/Self Investing/Projekti/Bad Art/Podatci za analizu/Nocturnal_forest_Gabon.wav' )
s_eur_wren, fs_eur_wren= sound.load('C:/Users/Korisnik/OneDrive - Prirodoslovno-matematički fakultet/Self Investing/Projekti/Bad Art/Podatci za analizu/Eurasian_wren.wav' )
s_frog_insect, fs_frog_insect= sound.load('C:/Users/Korisnik/OneDrive - Prirodoslovno-matematički fakultet/Self Investing/Projekti/Bad Art/Podatci za analizu/Frog_and_insect_chorus_Peru.wav' )
s_falcon, fs_falcon= sound.load('C:/Users/Korisnik/OneDrive - Prirodoslovno-matematički fakultet/Self Investing/Projekti/Bad Art/Podatci za analizu/Laughing_falcon.wav' )
s_brazil, fs_brazil= sound.load('C:/Users/Korisnik/OneDrive - Prirodoslovno-matematički fakultet/Self Investing/Projekti/Bad Art/Podatci za analizu/Quiet_Brazil.wav' )
s_synth_silence, fs_synth_silence= sound.load('C:/Users/Korisnik/OneDrive - Prirodoslovno-matematički fakultet/Self Investing/Projekti/Bad Art/Podatci za analizu/Synthesised_Silence.wav' )
s_savanna, fs_savanna= sound.load('C:/Users/Korisnik/OneDrive - Prirodoslovno-matematički fakultet/Self Investing/Projekti/Bad Art/Podatci za analizu/rock_savanna.wav' )
s_synth_white, fs_synth_white= sound.load('C:/Users/Korisnik/OneDrive - Prirodoslovno-matematički fakultet/Self Investing/Projekti/Bad Art/Podatci za analizu/Synthesised_Total_white_noise.wav' )
s_new_cald, fs_new_cald= sound.load('C:/Users/Korisnik/OneDrive - Prirodoslovno-matematički fakultet/Self Investing/Projekti/Bad Art/Podatci za analizu/Diurnal_shrubland_1_New_Caledonia.wav' )
s_for_Peru, fs_for_Peru= sound.load('C:/Users/Korisnik/OneDrive - Prirodoslovno-matematički fakultet/Self Investing/Projekti/Bad Art/Podatci za analizu/Evening_forest_Peru.wav' )
s_jackhammer, fs_jackhamemr= sound.load('C:/Users/Korisnik/OneDrive - Prirodoslovno-matematički fakultet/Self Investing/Projekti/Bad Art/Podatci za analizu/Jackhammer.wav' )
s_rain_gab, fs_rain_gab= sound.load('C:/Users/Korisnik/OneDrive - Prirodoslovno-matematički fakultet/Self Investing/Projekti/Bad Art/Podatci za analizu/Rain_in_forest_Gabon.wav' )
s_diur_gab, fs_diur_gab= sound.load('C:/Users/Korisnik/OneDrive - Prirodoslovno-matematički fakultet/Self Investing/Projekti/Bad Art/Podatci za analizu/Diurnal_forest_Gabon.wav' )
'''

#lista varijabli koji se koriste za obradu unutar for petlje
#S=[s_dinamo, s_dnova, s_fanfare, s_reklame,  s_direkt,  s_spidey,  s_jala,  s_jbp, s_lasagna,  s_peki,  s_spectre,  s_zzk, s_got, s_kor, s_nocfor_Gab,  s_brazil, s_diur_gab, s_eur_wren, s_falcon, s_for_Peru, s_frog_insect, s_jackhammer, s_rain_gab, s_savanna, s_synth_silence, s_synth_white]
#FS=[fs_dinamo, fs_dnova, fs_fanfare, fs_reklame, fs_direkt, fs_spidey, fs_jala, fs_jbp, fs_lasagna, fs_peki, fs_spectre, fs_zzk, fs_got, fs_kor, fs_nocfor_Gab, fs_brazil, fs_diur_gab, fs_eur_wren, fs_falcon, fs_for_Peru, fs_frog_insect, fs_jackhamemr, fs_rain_gab, fs_savanna, fs_synth_silence, fs_synth_white]

#S=[s_dnova, s_fanfare, s_reklame,  s_direkt,  s_spidey,  s_jala, s_lasagna,  s_peki,  s_spectre] #to su samo oni koji ne trabju ikakvo filtriranje buke jer su sintetički
#FS=[fs_dnova, fs_fanfare, fs_reklame, fs_direkt, fs_spidey, fs_jala, fs_lasagna, fs_peki, fs_spectre]
S=[s_vivaldi, s_mozart, s_pejacevic, s_fiori]
FS=[fs_vivaldi, fs_mozart, fs_pejacevic, fs_fiori]
row_names=['vivaldi', 'mozart', 'pejacevic', 'fiori']

#S = [s_nocfor_Gab,  s_brazil, s_diur_gab, s_eur_wren, s_falcon, s_for_Peru, s_frog_insect, s_jackhammer, s_rain_gab, s_savanna, s_synth_silence, s_synth_white]
#FS = [fs_nocfor_Gab,  fs_new_cald, fs_brazil, fs_diur_gab, fs_eur_wren, fs_falcon, fs_for_Peru, fs_frog_insect, fs_jackhamemr, fs_rain_gab, fs_savanna, fs_synth_silence, fs_synth_white]

#row_names=['dinamo','dnova','fanfare', 'reklame', 'direkt', 'spidey', 'jala', 'jbp', 'lasagna', 'peki', 'spectre', 'zizek','GoT','Predavanje','nocturanl_forest_Gabon', 'brazil','diurnal_forest_gabon', 'european wren', 'falcon', 'forest Peru', 'frogs and insects', 'jackhammer','rain forrest gabon', 'savanna','synthesized silence', 'synthesized white noise']
#row_names=['dnova','fanfare', 'reklame', 'direkt', 'spidey', 'jala', 'lasagna', 'peki', 'spectre']
#row_names=['nocturanl_forest_Gabon', 'brazil','diurnal_forest_gabon', 'european wren', 'falcon', 'forest Peru', 'frogs and insects', 'jackhammer','rain forrest gabon', 'savanna','synthesized silence', 'synthesized white noise']

column_names = ['median', 'tH','tActivity','ACI','fH','H of average spectrum','Kurt_spectral max','Skew spectral max','LFC','MFC',
               'HFC','soundscape index', 'Leq','LeqF_from spectrogram', 'AGI', 'bw50','bw90', 'tS2N', 'sS2N' ]



df = pd.DataFrame(index= row_names, columns=column_names )



for n in range(len(S)):
    
    #loads signal and sampling frequency from L
    s=S[n]
    fs=FS[n]

    print('now performing' + str(n))
    #generates spectrogram and converts is into dB spectrogram
    
    Sxx_P, tn, fn, ext=sound.spectrogram(s, fs)   
    #Sxx_A_noNoise, tna, fna, exta = sound.spectrogram(s, fs, mode= 'amplitude')
    Sxx_dB = util.power2dB(Sxx_P)+96 #I think that is only so that I have positive values
   
    #removes noise from the dB spectrogram
    Sxx_dB_noNoise, noise_profile, c = sound.remove_background(Sxx_dB)

    #converts denoised dB spectrogram back into power and amplitude spectrograms
    Sxx_A_noNoise=util.dB2amplitude(Sxx_dB_noNoise)
    Sxx_P_noNoise=util.dB2power(Sxx_dB_noNoise)

    #Analiza indeksima
    med = features.temporal_median(s)
    df.loc[row_names[n], 'median'] = med

    tEntropy=features.temporal_entropy(s)
    df.loc[row_names[n], 'tH'] = tEntropy

    df.loc[row_names[n], 'tActivity'], count, mean= features.temporal_activity(s,6)

    a ,b , df.loc[row_names[n], 'ACI'] = features.acoustic_complexity_index(Sxx_A_noNoise)

    df.loc[row_names[n], 'fH'], Ht_per_bin= features.frequency_entropy(Sxx_P_noNoise)

    df.loc[row_names[n], 'H of average spectrum'], ECU, ECV, EPS, df.loc[row_names[n], 'Kurt_spectral max'], df.loc[row_names[n], 'Skew spectral max'] = features.spectral_entropy(Sxx_P_noNoise, fn, flim=(20,20000)) #EAS, EPS_KURT, EPS_SKEW idu u df

    df.loc[row_names[n], 'LFC'], df.loc[row_names[n], 'MFC'], df.loc[row_names[n], 'HFC'] = features.spectral_cover(Sxx_dB_noNoise, fn) #

    df.loc[row_names[n], 'soundscape index'], ratioBA, antroPh, bioPh  = features.soundscape_index(Sxx_P_noNoise,fn,R_compatible=None)

    df.loc[row_names[n], 'Leq'] = maad.features.temporal_leq (s, fs, gain=42)

    df.loc[row_names[n], 'LeqF_from spectrogram'], Leqf_per_bin = maad.features.spectral_leq(Sxx_P_noNoise, gain=42)
    
    a1, a2, df.loc[row_names[n], 'AGI'], a3  = maad.features.acoustic_gradient_index(Sxx_P, tn[1]-tn[0]) #Noise must remain, RAW SPECTROGRAM
    
    df.loc[row_names[n], 'bw50'], df.loc[row_names[n], 'bw90'] = features.spectral_bandwidth(s, fs, nperseg=1024) #bw_50 i bw_90

    a1,a2,df.loc[row_names[n], 'tS2N'] = maad.sound.temporal_snr(s)

    a1,a2, df.loc[row_names[n], 'sS2N'],a3, a4, a5 = maad.sound.spectral_snr(Sxx_P_noNoise) #snr
    
    


df.to_csv('C:/Users/Korisnik/OneDrive - Prirodoslovno-matematički fakultet/Self Investing/Projekti/Bad Art/Podatci za analizu/klasicna_fltrd.csv', index=True)

end_time = time.time()
duration = end_time - start_time
print(f"Duration: {duration} seconds")
