import numpy as np
import math
import scipy
from scipy.io import wavfile

# Functions related to sample conversion/slicing

def audio_slicer(audio_object, start_secs, end_secs):
    start_sample = int(start_secs * audio_object.samplerate)
    end_sample = int(end_secs * audio_object.samplerate)
    processed_data = []
    for i in audio_object.signal:
        sliced_signal = i[start_sample:end_sample]
        sliced_time = i[start_sample:end_sample]
        processed_data.append(sliced_signal)
    sliced_time = audio_object.signal[0][start_sample:end_sample]
    audio_object.signal = processed_data
    audio_object.time_axis = sliced_time

    return audio_object

def audio_reverse(audio_object):
    audio_object.signal = np.flip(audio_object.signal)

# Functions related to Gain (addition/subtraction/calculation/conversion)

def audio_amplify_dbfs(audio_object, gain_dbfs):
    processed_arrays = []
    amplitude_multiplier = 10 ** (gain_dbfs / 20)
    for i in audio_object.signal:
        audio_array = amplitude_multiplier * i
        if (audio_array > 1.0).any() or (audio_array < -1.0).any():
            print('Signal is clipped')
        audio_array[audio_array > 1.0] = 1.0
        audio_array[audio_array < -1.0] = -1.0
        processed_arrays.append(audio_array)
    audio_object.signal = processed_arrays

    return audio_object

def audio_parameter_calc(audio_object, print_out = False):
    peak_list = []
    rms_list = []
    crest_factor_list = []
    for i in audio_object.signal:
        peak = max(i)
        peak_db = round((20 * np.log10(1/peak))*-1,2)
  
        rms = np.sqrt(np.mean(i**2))
        rms_db = round((20 * np.log10(1/rms))*-1,2)

        crest_factor = round(20 * np.log10(peak/rms),2)
        peak_list.append(peak_db)
        rms_list.append(rms_db)
        crest_factor_list.append(crest_factor)

    if print_out == True:
        print("Crest Factor (dB): ", crest_factor)
        print("Peak (dB): ", peak_db)
        print("RMS (dB): ", rms_db)

    audio_object.peak_db = peak_list
    audio_object.rms_db = rms_list
    audio_object.crest_factor = crest_factor_list

    #return crest_factor, peak_db, rms_db

# Functions related to time/frequency domain conversion

def audio_fft_convert(
        audio_object, 
        save_to_file = False, 
        file_name = None):
    fft_db_list = []

    duration = len(audio_object.signal[0]) / audio_object.samplerate
    fft_freqs = scipy.fft.fftfreq(int(audio_object.samplerate * duration), 1 / audio_object.samplerate)
    fft_data_length = int(len(fft_freqs) / 2)
    fft_freqs = fft_freqs[:fft_data_length]
    fft_freqs = np.array(fft_freqs)
    audio_object.fft_freqs = fft_freqs

    for i in audio_object.signal:
        fft_array = scipy.fft.fft(i)
        reference = max(abs(fft_array)) # 0dB becomes Maximum Amplitude
        fft_db = []

        for k in fft_array:
            fft_db.append(20 * math.log10(abs(k) / reference))

        fft_db = fft_db[:fft_data_length]
        fft_db = np.array(fft_db)
        fft_db_list.append(fft_db)
    audio_object.fft_db = fft_db_list

    if save_to_file == True:
        fft_data = []
        fft_data.append(fft_freqs)
        for i in fft_db_list:
            fft_data.append(i)
        fft_data = np.array(fft_data)
        fft_data = np.transpose(fft_data)
        np.savetxt(file_name+".csv", fft_data, header="Frequency (Hz), Level (dB)", delimiter=',')

def audio_envelope_follower(audio_object, frame_size, hop_length):
    envelope_data = []
    envelope_times = []
    for i in audio_object.signal:
        amplitude_envelope = []

    # Calculate amplitiude envelope for each frame

        for k in range(0, len(i), hop_length):
            current_frame_ae = max(i[k:k+frame_size])
            amplitude_envelope.append(current_frame_ae)
    
        frames = range(0,len(amplitude_envelope))
        times=[]
        for f in frames:
            times.append(f * hop_length/audio_object.samplerate)
        envelope_data.append(amplitude_envelope)
        envelope_times.append(times)
    audio_object.env_amplitude = envelope_data
    audio_object.env_time = envelope_times

# Functions related to exporting of audio data

def audio_export(audio_object, file_name):
    data_list=[]
    for i in audio_object.signal:
        i = i * 2**15
        data = i.astype(np.int16)
        data_list.append(data)
    data_array = np.array(data_list)
    data_array = np.transpose(data_array)
    wavfile.write(str(file_name)+".wav", audio_object.samplerate, data_array)