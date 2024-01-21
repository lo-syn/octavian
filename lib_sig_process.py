import numpy as np
import scipy
from scipy.io import wavfile
import math
import csv

# Functions related to sample conversion/slicing

def audio_slicer(input_array, start_secs, end_secs, fs):
    start_sample = int(start_secs * fs)
    end_sample = int(end_secs * fs)
    array_slice = input_array[start_sample:end_sample]

    return array_slice

# Functions related to Gain (addition/subtraction/calculation/conversion)

def amplify_dbfs(gain_dbfs,audio_array):
    amplitude_multiplier = 10 ** (gain_dbfs / 20)
    audio_array = amplitude_multiplier * audio_array
    if (audio_array > 1.0).any() or (audio_array < -1.0).any():
        print('Signal is clipped')
    audio_array[audio_array > 1.0] = 1.0
    audio_array[audio_array < -1.0] = -1.0

    return audio_array

def crest_factor_calc(audio_array, print_out):
    peak = max(audio_array[1])
    peak_db = round((20 * np.log10(1/peak))*-1,2)
  
    rms = np.sqrt(np.mean(audio_array[1]**2))
    rms_db = round((20 * np.log10(1/rms))*-1,2)

    crest_factor = round(20 * np.log10(peak/rms),2)

    if print_out == True:
        print("Crest Factor (dB): ", crest_factor)
        print("Peak (dB): ", peak_db)
        print("RMS (dB): ", rms_db)

    return crest_factor, peak_db, rms_db

# Functions related to time/frequency domain conversion

def fft_convert(audio_array, fs, save_to_file, file_name):
    duration = len(audio_array[1]) / fs
    fft_array = scipy.fft.fft(audio_array[1])
    fft_freq = scipy.fft.fftfreq(int(fs * duration), 1 / fs)

    reference = max(abs(fft_array)) # 0dB becomes Maximum Amplitude
    fft_db = []

    for i in fft_array:
        fft_db.append(20 * math.log10(abs(i) / reference))

    fft_data_length = int(len(fft_freq) / 2)
    fft_db = fft_db[:fft_data_length]
    fft_freq = fft_freq[:fft_data_length]
    fft_freq = np.array(fft_freq)
    fft_db = np.array(fft_db)
    fft_data = np.stack(((fft_freq,fft_db)))
    fft_data = np.transpose(fft_data)

    if save_to_file == True:
        np.savetxt(file_name+".csv", fft_data, header="Frequency (Hz), Level (dB)", delimiter=',')

    return fft_data

# Functions related to windowing / fade ins/outs

def hanning_window(audio_array):
    hanning_window = np.hanning(len(audio_array))
    windowed_array = hanning_window * audio_array

    return windowed_array

# Functions related to biquad filters

def biquad_sos_export(sos, fs, file_name) -> None:

    # SOS format is [b0,b1,b2,1,a1,a2]

    w, h = scipy.signal.sosfreqz(sos, worN=fs, fs=fs)

    db = 20 * np.log10(np.maximum(np.abs(h), 1e-5))

    with open(str(file_name)+".csv", "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=",")
        csvwriter.writerow(("Frequency", "Level (dB)"))
        for i in range(len(h)):
            csvwriter.writerow((w[i], 20 * np.log10(abs(h[i]))))  # WRITE TO CSV


def biquad_ba_export(B, A, fs, file_name):
    w, h = scipy.signal.freqz(B, A, worN=fs, fs=fs)

    db = 20 * np.log10(np.maximum(np.abs(h), 1e-5))

    with open(str(file_name)+".csv", "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=",")
        csvwriter.writerow(("Frequency", "Level (dB)"))
        for i in range(len(h)):
            csvwriter.writerow((w[i], 20 * np.log10(abs(h[i]))))  # WRITE TO CSV

# Functions related to exporting of audio data

def wav_export(audio_array, file_name):
    audio_array = audio_array[1] * 2**15
    data = audio_array.astype(np.int16)
    wavfile.write(str(file_name)+".wav", 48000, data)
