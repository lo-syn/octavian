"""
PyAudio Example: Make a wire between input and output (i.e., record a
few samples and play them back immediately).

This is the callback (non-blocking) version.
"""

import pyaudio
import time
import numpy as np
import pyqtgraph as pg
import sys
from PyQt5.QtWidgets import *
from scipy.fft import fft, fftfreq

app = QApplication(sys.argv)  # Create QApplication ***

def byte_to_float(byte):
    # byte -> int16(PCM_16) -> float32
    return pcm2float(np.frombuffer(byte,dtype=np.int16), dtype='float32')

def pcm2float(sig, dtype='float32'):
    """Convert PCM signal to floating point with a range from -1 to 1.
    Use dtype='float32' for single precision.
    Parameters
    ----------
    sig : array_like
        Input array, must have integral type.
    dtype : data type, optional
        Desired (floating point) data type.
    Returns
    -------
    numpy.ndarray
        Normalized floating point data.
    See Also
    --------
    float2pcm, dtype
    """
    sig = np.asarray(sig)
    if sig.dtype.kind not in 'iu':
        raise TypeError("'sig' must be an array of integers")
    dtype = np.dtype(dtype)
    if dtype.kind != 'f':
        raise TypeError("'dtype' must be a floating point type")

    i = np.iinfo(sig.dtype)
    abs_max = 2 ** (i.bits - 1)
    offset = i.min + abs_max
    return (sig.astype(dtype) - offset) / abs_max

WIDTH = 2
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()

rms = None
raw_data = None
def callback(in_data, frame_count, time_info, status):
    global rms
    global raw_data
    raw_data = in_data
    return in_data, pyaudio.paContinue


stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                stream_callback=callback)

stream.start_stream()
time.sleep(0.5)
while stream.is_active():
    integer_data = byte_to_float(raw_data)
    yf = fft(integer_data)
    T = 1 / 44100
    xf = fftfreq(576, T)[:576//2]
    
    break

win = pg.GraphicsLayoutWidget(title="Spectrogram") # creates a window
p1 = win.addPlot(title="Spectrogram", row=0,col=0)  # creates empty space for the plot in the window
p2 = win.addPlot(title="Time Domain",row=1,col=0)
win.setGeometry(100, 100, 800, 600)

#help(win)

p1.setLogMode(True,True)
p1.showGrid(True,True)
p1.setYRange(-6, 0, padding=0)

p2.setYRange(-0.05, 0.05)

curve_freq = p1.plot()                       # create an empty "plot" (a curve to plot)#
curve_time = p2.plot()


#windowWidth = 500                       # width of the window displaying the curve
#Xm = np.linspace(0,0,576)          # create array that will contain the relevant time series     
#ptr = -windowWidth

windowWidth = xf                       # width of the window displaying the curve
Xm = np.linspace(0,0,len(yf))         # create array that will contain the relevant freq series     
ptr = 0

win.show() # you need to add this 


# Realtime data plot. Each time this function is called, the data display is updated
def update():
    global curve, ptr, Xm    
    #Xm[:-1] = Xm[1:]                      # shift data in the temporal mean 1 sample left
    value = integer_data               # read line (single value) from the serial port
    Xm = value               # vector containing the instantaneous values      
    ptr += 576                             # update x position for displaying the curve
    curve_time.setData(Xm)                     # set the curve with this data
    curve_time.setPos(ptr,0)                   # set x position in the graph to 0
    QApplication.processEvents()    # you MUST process the plot now

def update_fft():
    global curve, ptr, Xm                       # shift data in the temporal mean 1 sample left
    value = 2.0/576 * np.abs(yf[0:576//2])            # read line (single value) from the serial port
    Xm = value               # vector containing the instantaneous values                      
    curve_freq.setData(xf,Xm)                   # set the curve with this data
    #print(help(curve_freq))
    #curve.setPos(ptr,0)                   # set x position in the graph to 0
    QApplication.processEvents()    # you MUST process the plot now

x = np.zeros(288)

while stream.is_active():  # <--------------------------------------------

    integer_data = byte_to_float(raw_data)
    #print(len(integer_data))
    yf = fft(integer_data)
    T = 1.0 / 44100.0
    xf = fftfreq(576, T)[:576//2]

    update_fft()
    update()


    x +=0.01

    y = np.linspace(0,1,len(yf))
    freq_spec = 2.0/576 * np.abs(yf[0:576//2])  
    z = (freq_spec - min(freq_spec)) / ( max(freq_spec) - min(freq_spec))
    y = np.linspace(0,1,len(freq_spec))
    


    pts = np.vstack([x,y,z]).transpose()


    
    #plt = gl.GLLinePlotItem(pos=pts)

    #view.addItem(plt)

    time.sleep(1/(44100/576))
app.exec_()  # Start QApplication event loop ***


    

stream.stop_stream()
stream.close()

p.terminate()