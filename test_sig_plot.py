from sig_plot import *
from sine_burst import SineBurst
from noise import Noise
from audiofile import AudioFile
from sig_process import audio_fft_convert,audio_envelope_follower

file_path = r"C:\Users\laure\OneDrive\Documents\Octavian\4AM.wav"

pink_noise = Noise(-3,3,48000, pinking_filter=True)
white_noise = Noise(-3,3,48000, pinking_filter=False)
sine_burst = SineBurst(1000,-3,1,48000)
audio_file = AudioFile(file_path)
audio_fft_convert(pink_noise)
audio_fft_convert(white_noise)
audio_fft_convert(sine_burst)
audio_fft_convert(audio_file)

app = init_plot()
window = create_window()
freq_plot = add_freq_plot(window,0,0,legend=True)
update_freq_plot(pink_noise,freq_plot,0,pink_noise.name)
update_freq_plot(white_noise,freq_plot,1,white_noise.name)
update_freq_plot(sine_burst,freq_plot,2,sine_burst.name)
update_freq_plot(audio_file,freq_plot,3,audio_file.name)

time_plot = add_time_plot(window,1,0,legend=True)
update_time_plot(pink_noise,time_plot,0,pink_noise.name)
update_time_plot(white_noise,time_plot,1,white_noise.name)
update_time_plot(sine_burst,time_plot,2,sine_burst.name)
update_time_plot(audio_file,time_plot,3,audio_file.name)

audio_envelope_follower(pink_noise, 1024, 512)
audio_envelope_follower(white_noise, 1024, 512)
audio_envelope_follower(sine_burst, 1024, 512)
audio_envelope_follower(audio_file, 1024, 512)

time_env_plot = add_time_plot(window,2,0,legend=True)

update_time_envelope_plot(pink_noise,time_env_plot,0,pink_noise.name)
update_time_envelope_plot(white_noise,time_env_plot,1,white_noise.name)
update_time_envelope_plot(sine_burst,time_env_plot,2,sine_burst.name)
update_time_envelope_plot(audio_file,time_env_plot,3,audio_file.name)

#add_time_plot(audio_object,window,1,0)
#add_label(window, f"Peak: {audio_object.peak_db}dB")
#add_label(window, f"RMS: {audio_object.rms_db}dB")
#add_label(window, f"Crest Factor: {audio_object.crest_factor}dB")

exec_plot(app)