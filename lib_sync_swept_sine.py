import math
import numpy as np
from scipy import signal
from scipy.fft import fft, ifft

from lib_sig_process import wav_export, amplify_dbfs
from lib_sig_plot import *

FS = 48000

def swept_sine(f1, f2, fs, time):
    '''
    This function generates an exponential sine sweep
    It is a Python implementation of the Matlab code found in Synchronized Sine Sweep paper
    '''
    L = time / math.log(f2/f1)
    t = np.arange(0,(fs*time)-1)/ fs
    x = np.sin(2* math.pi *f1 *L*(np.exp(t/L)))

    return x, L

def sine_sweep_windowing(sine_sweep_array, fs):
    '''
    This function applies a cosine window to fs/10 at the start and end of the signal
    '''
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

def deconvolve(input_array, L, f1, fs):

    length = 2**math.ceil(math.log2(len(input_array)))

    Y = np.fft.fft(input_array,length) / fs 

    f_ax = np.linspace(0, fs, length+1)
    spectrum = np.zeros_like(f_ax, dtype=np.complex_)
    #  X = 2*sqrt(f ax/L).*exp(−j*2*pi* f ax*L.*(1−log(f ax/f1)) + j*pi/4) .                      
    spectrum[1:] = 2*np.sqrt(f_ax[1:]/L) * np.exp(-2j * np.pi*f_ax[1:]*L* (1 - np.log(f_ax[1:]/f1))+ 1j * np.pi/4)
    #remainder, H = signal.deconvolve(Y, X)
    ##2*sqrt(f_ax/L) .* exp(−j*2*pi*

    H = Y*spectrum[1:]
    #H = signal.deconvolve(input_array, X)
    #H[1] = 0

    h = np.fft.ifft(H) # Must be zymmetric?
   #print(h)

    
    return h

    

x, L = swept_sine(20,20000,FS,1)

sine_x = sine_sweep_windowing(x, FS)

sine_x = amplify_dbfs(3, sine_x)

h = deconvolve(sine_x, L, 20, FS)
#y = np.array(abs(y))
#x = np.array(abs(x))
# 
#freq_resp  = np.stack((y,x))
#print(freq_resp[0])

sine_sweep = np.vstack((sine_x,np.arange(0,len(sine_x))))

#app = init_plot()
#window = create_window()
#add_freq_plot(freq_resp, window,1,2,3)
#add_time_plot(sine_sweep, window)
#app.exec_()
import matplotlib.pyplot as plt
plt.plot(h)
plt.grid()
plt.show()

wav_export(h, 48000, "sine")
