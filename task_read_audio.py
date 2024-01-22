from lib_audio_read import *
from lib_sig_process import *
from lib_sig_plot import *

filename = r"C:\Users\laurence.porter\Documents\Test_Development\Octavian\10ms_burst.wav"

audio_data = audio_file_read(filename)
print(audio_data)

