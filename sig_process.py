import numpy as np
import math
import scipy
from scipy.io import wavfile

# Functions related to sample conversion/slicing

def audio_slicer(audio_object, start_secs, end_secs):
    start_sample = int(start_secs * audio_object.samplerate)
    end_sample = int(end_secs * audio_object.samplerate)
    audio_object.signal = audio_object.signal[start_sample:end_sample]
    audio_object.time_axis = audio_object.time_axis[start_sample:end_sample]

    return audio_object

def audio_reverse(audio_object):
    audio_object.signal = np.flip(audio_object.signal)

# Functions related to Gain (addition/subtraction/calculation/conversion)

def audio_amplify_dbfs(audio_object, gain_dbfs):
    amplitude_multiplier = 10 ** (gain_dbfs / 20)
    audio_array = amplitude_multiplier * audio_object.signal
    if (audio_array > 1.0).any() or (audio_array < -1.0).any():
        print('Signal is clipped')
    audio_array[audio_array > 1.0] = 1.0
    audio_array[audio_array < -1.0] = -1.0
    audio_object.signal = audio_array

    return audio_object

def audio_parameter_calc(audio_object, print_out = False):
    peak = max(audio_object.signal)
    peak_db = round((20 * np.log10(1/peak))*-1,2)
  
    rms = np.sqrt(np.mean(audio_object.signal**2))
    rms_db = round((20 * np.log10(1/rms))*-1,2)

    crest_factor = round(20 * np.log10(peak/rms),2)

    if print_out == True:
        print("Crest Factor (dB): ", crest_factor)
        print("Peak (dB): ", peak_db)
        print("RMS (dB): ", rms_db)

    audio_object.peak_db = peak_db
    audio_object.rms_db = rms_db
    audio_object.crest_factor = crest_factor

    return crest_factor, peak_db, rms_db

# Functions related to time/frequency domain conversion

def audio_fft_convert(
        audio_object, 
        save_to_file = False, 
        file_name = None):
    duration = len(audio_object.signal) / audio_object.samplerate
    fft_array = scipy.fft.fft(audio_object.signal)
    fft_freqs = scipy.fft.fftfreq(int(audio_object.samplerate * duration), 1 / audio_object.samplerate)

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

def audio_envelope_follower(audio_object, frame_size, hop_length):
    amplitude_envelope = []

    # Calculate amplitiude envelope for each frame

    for i in range(0, len(audio_object.signal), hop_length):
        current_frame_ae = max(audio_object.signal[i:i+frame_size])
        amplitude_envelope.append(current_frame_ae)
    
    frames = range(0,len(amplitude_envelope))
    times=[]
    for i in frames:
        times.append(i * hop_length/audio_object.samplerate)
    audio_object.env_amplitude = amplitude_envelope
    audio_object.env_time = times

# Functions related to exporting of audio data

def audio_export(audio_object, file_name):

    audio_array = audio_object.signal * 2**15
    data = audio_array.astype(np.int16)
    wavfile.write(str(file_name)+".wav", audio_object.samplerate, data)