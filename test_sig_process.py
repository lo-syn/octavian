import matplotlib.pyplot as plt
from sine_burst import SineBurst
from sine_sweep import SineSweep
from noise import Noise
sine_burst = SineBurst(1000, -3, 1, 48000, windowed=False)
sine_sweep = SineSweep(20,200, -3, 1, 48000, windowed=False)
white_noise = Noise(-3, 1, 48000, pinking_filter=False)

def audio_slicer(audio_object, start_secs, end_secs, fs):
    start_sample = int(start_secs * fs)
    end_sample = int(end_secs * fs)
    audio_object.signal = audio_object.signal[start_sample:end_sample]
    audio_object.time_axis = audio_object.time_axis[start_sample:end_sample]

    return audio_object

sine_burst = audio_slicer(sine_burst, 0, 0.55, sine_burst.samplerate)
sine_sweep = audio_slicer(sine_sweep, 0, 0.55, sine_sweep.samplerate)
white_noise = audio_slicer(white_noise, 0, 0.55, white_noise.samplerate)


