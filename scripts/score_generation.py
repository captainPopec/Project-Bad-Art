"""
Acoustic index scoring for WAV files in ../data/.
Outputs a CSV with one row per file and 19 acoustic indices as columns.
"""

import os
import glob
import time

import maad
from maad import sound, features, util
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
OUTPUT_CSV = os.path.join(os.path.dirname(__file__), '..', 'scores.csv')

COLUMNS = [
    'median', 'tH', 'tActivity', 'ACI', 'fH', 'H_of_avg_spectrum',
    'Kurt_spectral_max', 'Skew_spectral_max', 'LFC', 'MFC', 'HFC',
    'soundscape_index', 'Leq', 'LeqF_from_spectrogram', 'AGI',
    'bw50', 'bw90', 'tS2N', 'sS2N',
]


def compute_scores(wav_path):
    s, fs = sound.load(wav_path)

    Sxx_P, tn, fn, ext = sound.spectrogram(s, fs)
    Sxx_dB = util.power2dB(Sxx_P) + 96

    # Remove stationary background noise before computing spectral indices
    Sxx_dB_noNoise, _, _ = sound.remove_background(Sxx_dB)
    Sxx_A_noNoise = util.dB2amplitude(Sxx_dB_noNoise)
    Sxx_P_noNoise = util.dB2power(Sxx_dB_noNoise)

    row = {}
    row['median'] = features.temporal_median(s)
    row['tH'] = features.temporal_entropy(s)
    row['tActivity'], _, _ = features.temporal_activity(s, 6)
    _, _, row['ACI'] = features.acoustic_complexity_index(Sxx_A_noNoise)
    row['fH'], _ = features.frequency_entropy(Sxx_P_noNoise)

    (row['H_of_avg_spectrum'], _, _, _,
     row['Kurt_spectral_max'], row['Skew_spectral_max']) = features.spectral_entropy(
        Sxx_P_noNoise, fn, flim=(20, 20000)
    )

    row['LFC'], row['MFC'], row['HFC'] = features.spectral_cover(Sxx_dB_noNoise, fn)

    row['soundscape_index'], _, _, _ = features.soundscape_index(
        Sxx_P_noNoise, fn, R_compatible=None
    )

    row['Leq'] = features.temporal_leq(s, fs, gain=42)
    row['LeqF_from_spectrogram'], _ = features.spectral_leq(Sxx_P_noNoise, gain=42)

    # AGI requires the raw (non-denoised) spectrogram
    _, _, row['AGI'], _ = features.acoustic_gradient_index(Sxx_P, tn[1] - tn[0])

    row['bw50'], row['bw90'] = features.spectral_bandwidth(s, fs, nperseg=1024)

    _, _, row['tS2N'] = maad.sound.temporal_snr(s)
    _, _, row['sS2N'], _, _, _ = maad.sound.spectral_snr(Sxx_P_noNoise)

    return row


def main():
    wav_files = sorted(
        glob.glob(os.path.join(DATA_DIR, '**', '*.wav'), recursive=True) +
        glob.glob(os.path.join(DATA_DIR, '**', '*.WAV'), recursive=True)
    )

    if not wav_files:
        print(f'No WAV files found in {DATA_DIR}')
        return

    rows = {}
    for path in wav_files:
        name = os.path.splitext(os.path.basename(path))[0]
        print(f'Processing: {name}')
        t0 = time.time()
        rows[name] = compute_scores(path)
        print(f'  done in {time.time() - t0:.1f}s')

    df = pd.DataFrame.from_dict(rows, orient='index', columns=COLUMNS)
    df.to_csv(OUTPUT_CSV, index=True)
    print(f'\nSaved {len(rows)} rows to {OUTPUT_CSV}')


if __name__ == '__main__':
    main()
