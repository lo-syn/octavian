from sig_plot import *
from sine_burst import SineBurst
from sig_process import audio_fft_convert

sine_burst = SineBurst(1000, -2, 1, 48000, windowed=False)
audio_fft_convert(sine_burst)

app = init_plot()
window = create_window()
add_freq_plot(sine_burst,window)
add_time_plot(sine_burst,window)
exec_plot(app)