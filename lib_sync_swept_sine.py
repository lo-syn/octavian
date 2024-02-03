import math
import numpy as np
from scipy import signal

from lib_sig_process import wav_export

def swept_sine(f1, f2, fs, time):
    L = time / math.log(f2/f1)
    t = np.arange(0,(fs*time)-1)/ fs
    x = np.sin(2* math.pi *f1 *L*(np.exp(t/L)))

    return x

def sine_sweep_windowing(sine_sweep_array, fs):
    fd1 = int(fs / 10)
    window= signal.windows.cosine(fd1-1)
    fade = np.arange(0, fd1-1, dtype=int)
    #fade in = (1−cos((0:fd1−1)/fd1*pi))/2;

    fade_in = (1 - np.cos(fade/fd1*math.pi))/2
    fade_out = np.flip(fade_in)
    idx = np.arange(1,fd1)
    sine_sweep_array[idx]=sine_sweep_array[idx] * fade_in
    sine_sweep_array[-fd1+1::]=sine_sweep_array[-fd1+1::] * fade_out

    return sine_sweep_array

x = swept_sine(20,20000,48000,1)

x = sine_sweep_windowing(x, 48000)


wav_export(x, 48000, "sine")
