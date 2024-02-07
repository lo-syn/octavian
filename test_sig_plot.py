from sig_plot import *
from sine_burst import SineBurst
from sig_process import audio_fft_convert, audio_parameter_calc


sine_burst = SineBurst(1000, -2, 1, 48000, windowed=False)
audio_fft_convert(sine_burst)
audio_parameter_calc(sine_burst)

app = init_plot()
window = create_window()
add_freq_plot(sine_burst,window,0,0)
add_time_plot(sine_burst,window,1,0)
add_label(window, f"Peak: {sine_burst.peak_db}dB")
add_label(window, f"RMS: {sine_burst.rms_db}dB")
add_label(window, f"Crest Factor: {sine_burst.crest_factor}dB")

exec_plot(app)