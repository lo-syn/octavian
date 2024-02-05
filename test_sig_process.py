import matplotlib.pyplot as plt
from sine_burst import SineBurst
from sine_sweep import SineSweep
from noise import Noise
import numpy as np

sine_burst = SineBurst(1000, -2, 1, 48000, windowed=False)
sine_sweep = SineSweep(20,200, -3, 1, 48000, windowed=False)
white_noise = Noise(-3, 1, 48000, pinking_filter=False)

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

sine_burst = audio_slicer(sine_burst, 0, 0.55, sine_burst.samplerate)
sine_sweep = audio_slicer(sine_sweep, 0, 0.55, sine_sweep.samplerate)
white_noise = audio_slicer(white_noise, 0, 0.55, white_noise.samplerate)

sine_burst = audio_amplify_dbfs(sine_burst, 3)

audio_parameter_calc(sine_sweep, True)
print(sine_sweep.rms_db)




