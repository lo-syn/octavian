from octavian.lib_sig_gen_REDUNDANT import *
from lib_sig_process import *
from lib_sig_plot import *

FS = 48000

sine = sine_wave_gen(100,FS,1,-12)
sweep = sine_sweep_gen(20,20000,FS,1,-6)
noise = noise_gen(FS, 1,"pink",-3)

audio = sine

# Logarithmic Gain addition/reduction

#ToDo: Fix wraparound problem at 1.0 peak
audio = amplify_dbfs(13,audio)
audio = amplify_dbfs(-1,audio)

# Slicing audio

#audio = audio_slicer(audio[1],0.1,0.3,FS)

# Calculate signal parameters

crest_factor, rms, peak = crest_factor_calc(audio, print_out=True)

# Export Frequency data 

fft_data=fft_convert(audio,FS,save_to_file=True,file_name="sine_fft")

# Conversion to int16 and export

wav_export(audio,"clipped_sine_-3dBFS")

# Graph plotting

app = init_plot()
window = create_window()
add_freq_plot(fft_data, window, rms, peak, crest_factor)
add_time_plot(audio, window)
app.exec_()



