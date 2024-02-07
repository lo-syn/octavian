from sig_plot import *
from sine_burst import SineBurst
from noise import Noise
from sig_process import audio_fft_convert, audio_parameter_calc


audio_object = Noise(-3,3,48000, pinking_filter=True)
audio_fft_convert(audio_object)
audio_parameter_calc(audio_object)

app = init_plot()
window = create_window()
add_freq_plot(audio_object,window,0,0)
add_time_plot(audio_object,window,1,0)
add_label(window, f"Peak: {audio_object.peak_db}dB")
add_label(window, f"RMS: {audio_object.rms_db}dB")
add_label(window, f"Crest Factor: {audio_object.crest_factor}dB")

exec_plot(app)