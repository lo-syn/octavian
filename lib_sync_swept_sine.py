import math
import numpy as np

from lib_sig_process import wav_export

def swept_sine(f1, f2, fs, time):
    L = time / math.log(f2/f1)
    t = np.arange(0,(fs*time)-1)/ fs
    x = np.sin(2* math.pi *f1 *L*(np.exp(t/L)))

    return x

x = swept_sine(20,20000,48000,1)

#wav_export(x, 48000, "sine")
