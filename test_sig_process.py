import matplotlib.pyplot as plt
from sine_burst import SineBurst
from sine_sweep import SineSweep
from noise import Noise
from audiofile import AudioFile

from sig_process import *

sine_burst = SineBurst(1000, -2, 1, 48000, windowed=False)
sine_sweep = SineSweep(20,200, -3, 1, 48000, windowed=False)
windowed_sweep = SineSweep(20,200, -3, 1, 48000, windowed=True)
white_noise = Noise(-3, 1, 48000, pinking_filter=False)
pink_noise = Noise(-3, 1, 48000, pinking_filter=True)
audio_file = AudioFile(r"4AM.wav")

audio_slicer(sine_burst, 0, 0.55)
audio_slicer(sine_sweep, 0, 0.55)
audio_slicer(windowed_sweep, 0, 0.55)
audio_slicer(white_noise, 0, 0.55)
audio_slicer(pink_noise, 0, 0.55)
audio_slicer(audio_file, 0, 0.55)

audio_reverse(sine_burst)
audio_reverse(sine_sweep)
audio_reverse(windowed_sweep)
audio_reverse(white_noise)
audio_reverse(pink_noise)
audio_reverse(audio_file) 

audio_amplify_dbfs(sine_burst, 3)
audio_amplify_dbfs(sine_sweep, -3)
audio_amplify_dbfs(windowed_sweep, -3)
audio_amplify_dbfs(white_noise, -12)
audio_amplify_dbfs(pink_noise, -12)
audio_amplify_dbfs(audio_file, -3)

audio_parameter_calc(sine_burst, True)
audio_parameter_calc(sine_sweep, True)
audio_parameter_calc(windowed_sweep, True)
audio_parameter_calc(white_noise, True)
audio_parameter_calc(pink_noise, True)
audio_parameter_calc(audio_file, True)

audio_fft_convert(sine_burst, True, "test_sine_fft")
audio_fft_convert(sine_sweep, True, "test_sine_sweep_fft")
audio_fft_convert(windowed_sweep, True, "test_windowed_sweep_fft")
audio_fft_convert(white_noise, True, "test_white_noise_fft")
audio_fft_convert(pink_noise, True, "test_pink_noise_fft")
audio_fft_convert(audio_file, True, "test_audio_file_fft")

audio_export(sine_burst, "test_sine_export")
audio_export(sine_sweep, "test_sine_sweep_export")
audio_export(windowed_sweep, "test_windowed_sweep_export")
audio_export(white_noise, "test_white_noise_export")
audio_export(pink_noise, "test_pink_noise_export")
audio_export(audio_file, "test_audio_file_export")

audio_envelope_follower(sine_burst, 1024, 512)
audio_envelope_follower(sine_sweep, 1024, 512)
audio_envelope_follower(windowed_sweep, 1024, 512)
audio_envelope_follower(white_noise, 1024, 512)
audio_envelope_follower(pink_noise, 1024, 512)
audio_envelope_follower(audio_file, 1024, 512)


#plt.plot(audio_file.env_time, audio_file.env_amplitude, color = 'r')
# plt.plot(sine_burst.fft_freqs, sine_burst.fft_db, color='r')
# plt.plot(sine_sweep.fft_freqs, sine_sweep.fft_db, color='b')
for i in range(len(sine_burst.fft_db)):
    plt.plot(audio_file.fft_freqs, audio_file.fft_db[i], color='b')

# plt.plot(white_noise.fft_freqs, white_noise.fft_db, color='g')
#plt.plot(audio_file.env_time[0], audio_file.env_amplitude[0], color='b')
#plt.plot(audio_file.env_time[1], audio_file.env_amplitude[1], color='r')
plt.title('FFT')
plt.ylabel('Amplitude')
plt.xlabel('Freq (Hz)')
plt.show()
print("pause for graph")




