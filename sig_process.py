import numpy as np
import math
import scipy

def audio_slicer(audio_object, start_secs, end_secs, fs):
    start_sample = int(start_secs * fs)
    end_sample = int(end_secs * fs)
    audio_object.signal = audio_object.signal[start_sample:end_sample]
    audio_object.time_axis = audio_object.time_axis[start_sample:end_sample]

    return audio_object

def audio_amplify_dbfs(audio_object, gain_dbfs):
    amplitude_multiplier = 10 ** (gain_dbfs / 20)
    audio_array = amplitude_multiplier * audio_object.signal
    if (audio_array > 1.0).any() or (audio_array < -1.0).any():
        print('Signal is clipped')
    audio_array[audio_array > 1.0] = 1.0
    audio_array[audio_array < -1.0] = -1.0
    audio_object.signal = audio_array

    return audio_object

def audio_parameter_calc(audio_object, print_out):
    peak = max(audio_object.signal)
    peak_db = round((20 * np.log10(1/peak))*-1,2)
  
    rms = np.sqrt(np.mean(audio_object.signal**2))
    rms_db = round((20 * np.log10(1/rms))*-1,2)

    crest_factor = round(20 * np.log10(peak/rms),2)

    if print_out == True:
        print("Crest Factor (dB): ", crest_factor)
        print("Peak (dB): ", peak_db)
        print("RMS (dB): ", rms_db)

    audio_object.peak_db = rms_db
    audio_object.rms_db = rms_db
    audio_object.crest_factor = crest_factor

    return crest_factor, peak_db, rms_db

def audio_fft_convert(audio_object, fs, save_to_file, file_name):
    duration = len(audio_object.signal) / fs
    fft_array = scipy.fft.fft(audio_object.signal)
    fft_freqs = scipy.fft.fftfreq(int(fs * duration), 1 / fs)

    reference = max(abs(fft_array)) # 0dB becomes Maximum Amplitude
    fft_db = []

    for i in fft_array:
        fft_db.append(20 * math.log10(abs(i) / reference))

    fft_data_length = int(len(fft_freqs) / 2)
    fft_db = fft_db[:fft_data_length]
    fft_freqs = fft_freqs[:fft_data_length]
    fft_freqs = np.array(fft_freqs)
    fft_db = np.array(fft_db)
    audio_object.fft_freqs = fft_freqs
    audio_object.fft_db = fft_db

    if save_to_file == True:
        fft_data = np.stack(((fft_freqs,fft_db)))
        fft_data = np.transpose(fft_data)
        np.savetxt(file_name+".csv", fft_data, header="Frequency (Hz), Level (dB)", delimiter=',')