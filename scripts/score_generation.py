
"""
Acoustic index scoring for WAV files in ../data/bio/ and ../data/antropo/.
Outputs scores.csv with one row per file: filename, group (A=antropo, B=bio),
and 19 acoustic indices. Runs in parallel across files; skips and logs errors.
"""

import csv
import glob
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

import maad
from maad import features, sound, util

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
OUTPUT_CSV = os.path.join(os.path.dirname(__file__), '..', 'scores.csv')
N_WORKERS = int(os.environ.get('SLURM_CPUS_PER_TASK', 8))

COLUMNS = [
    'filename', 'group',
    'median', 'tH', 'tActivity', 'ACI', 'fH', 'H_of_avg_spectrum',
    'Kurt_spectral_max', 'Skew_spectral_max', 'LFC', 'MFC', 'HFC',
    'soundscape_index', 'Leq', 'LeqF_from_spectrogram', 'AGI',
    'bw50', 'bw90', 'tS2N', 'sS2N',
]


def compute_scores(wav_path):
    s, fs = sound.load(wav_path)

    Sxx_P, tn, fn, ext = sound.spectrogram(s, fs)
    Sxx_dB = util.power2dB(Sxx_P) + 96

    Sxx_dB_noNoise, _, _ = sound.remove_background(Sxx_dB)
    Sxx_A_noNoise = util.dB2amplitude(Sxx_dB_noNoise)
    Sxx_P_noNoise = util.dB2power(Sxx_dB_noNoise)

    parent = os.path.basename(os.path.dirname(wav_path))
    group = 'A' if parent == 'antropo' else 'B'

    row = {
        'filename': os.path.splitext(os.path.basename(wav_path))[0],
        'group': group,
    }
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


def score_file(wav_path):
    t0 = time.time()
    try:
        row = compute_scores(wav_path)
        print(f'OK  {os.path.basename(wav_path)}  ({time.time() - t0:.1f}s)', flush=True)
        return row
    except Exception as e:
        print(f'SKIPPED {wav_path}: {e}', flush=True)
        return None


def main():
    wav_files = sorted(
        glob.glob(os.path.join(DATA_DIR, '**', '*.wav'), recursive=True) +
        glob.glob(os.path.join(DATA_DIR, '**', '*.WAV'), recursive=True)
    )

    if not wav_files:
        print(f'No WAV files found in {DATA_DIR}')
        return

    print(f'Found {len(wav_files)} files. Running with {N_WORKERS} workers.')

    completed = 0
    skipped = 0

    with open(OUTPUT_CSV, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=COLUMNS)
        writer.writeheader()

        with ProcessPoolExecutor(max_workers=N_WORKERS) as executor:
            futures = {executor.submit(score_file, p): p for p in wav_files}
            for future in as_completed(futures):
                row = future.result()
                if row is not None:
                    writer.writerow(row)
                    csvfile.flush()
                    completed += 1
                else:
                    skipped += 1

    print(f'\nDone. Scored: {completed}, Skipped: {skipped}. Output: {OUTPUT_CSV}')


if __name__ == '__main__':
    main()
