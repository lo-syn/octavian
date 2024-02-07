import matplotlib.pyplot as plt
from sine_burst import SineBurst
from sine_sweep import SineSweep
from noise import Noise
from audiofile import AudioFile

from sig_process import *

sine_burst = SineBurst(1000, -2, 1, 48000, windowed=False)
sine_sweep = SineSweep(20,200, -3, 1, 48000, windowed=False)
white_noise = Noise(-3, 1, 48000, pinking_filter=False)
audio_file = AudioFile(r"4AM.wav")

sine_burst = audio_slicer(sine_burst, 0, 0.55)
sine_sweep = audio_slicer(sine_sweep, 0, 0.55)
white_noise = audio_slicer(white_noise, 0, 0.55)
audio_file = audio_slicer(audio_file, 0, 1)

sine_burst = audio_amplify_dbfs(sine_burst, 3)
sine_sweep = audio_amplify_dbfs(sine_sweep, -3)
white_noise = audio_amplify_dbfs(white_noise, -12)
audio_file = audio_amplify_dbfs(audio_file, -3)

audio_parameter_calc(sine_burst, True)
audio_parameter_calc(sine_sweep, True)
audio_parameter_calc(white_noise, True)
audio_parameter_calc(audio_file, True) # DOESN'T WORK WITH MULTICHANNEL

audio_fft_convert(sine_burst, True, "test_sine_fft")
audio_fft_convert(sine_sweep, True, "test_sine_sweep_fft")
audio_fft_convert(white_noise, True, "test_white_noise_fft")
# audio_fft_convert(audio_file, True, "test_audio_file_fft") DOESN'T WORK WITH MULTICHANNEL

audio_export(sine_burst, "test_sine_export")
audio_export(sine_sweep, "test_sine_sweep_export")
audio_export(white_noise, "test_white_noise_export")
audio_export(audio_file, "test_audio_file_export")

audio_reverse(audio_file) 

# audio_envelope_follower(audio_file, 1024, 512) DOESN'T WORK WITH MULTICHANNEL


#plt.plot(audio_file.env_time, audio_file.env_amplitude, color = 'r')
# plt.plot(sine_burst.fft_freqs, sine_burst.fft_db, color='r')
# plt.plot(sine_sweep.fft_freqs, sine_sweep.fft_db, color='b')
# plt.plot(white_noise.fft_freqs, white_noise.fft_db, color='g')
plt.plot(audio_file.time_axis, audio_file.signal, color='b')
plt.title('FFT')
plt.ylabel('Amplitude')
plt.xlabel('Freq (Hz)')
plt.show()
print("pause for graph")



