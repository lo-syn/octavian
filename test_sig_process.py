import matplotlib.pyplot as plt
from sine_burst import SineBurst
from sine_sweep import SineSweep
from noise import Noise

from sig_process import *

sine_burst = SineBurst(1000, -2, 1, 48000, windowed=False)
sine_sweep = SineSweep(20,200, -3, 1, 48000, windowed=False)
white_noise = Noise(-3, 1, 48000, pinking_filter=False)


sine_burst = audio_slicer(sine_burst, 0, 0.55, sine_burst.samplerate)
sine_sweep = audio_slicer(sine_sweep, 0, 0.55, sine_sweep.samplerate)
white_noise = audio_slicer(white_noise, 0, 0.55, white_noise.samplerate)

sine_burst = audio_amplify_dbfs(sine_burst, 3)

audio_parameter_calc(sine_sweep, True)
print(sine_sweep.rms_db)

audio_fft_convert(sine_burst, sine_burst.samplerate, True, "test_sine_fft")

plt.plot(sine_burst.fft_freqs, sine_burst.fft_db, color='r')
plt.title('Sine FFT')
plt.ylabel('Amplitude')
plt.xlabel('Freq (Hz)')
plt.show()





