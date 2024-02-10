import pyqtgraph as pg
import numpy as np
import sys
from PyQt5.QtWidgets import *

def init_plot():
    app = QApplication(sys.argv)  # Create QApplication ***
    return app

def exec_plot(app):
    app.exec_()

def create_window(background_colour="k"):
    window = pg.GraphicsLayoutWidget()
    window.setGeometry(100, 100, 1400, 900)
    window.setBackground(background_colour)
    window.show()
    return window

def add_freq_plot(window, row, col, legend=False):
    p1 = window.addPlot(row=row,col=col)
    p1.setLabel(axis='bottom', text='Frequency', units='Hz')
    p1.setLabel(axis='left', text='Level', units='dB')
    p1.showGrid(x=True, y=True)   # To show grid lines across x axis and y axis
    p1.setLogMode(True)
    if legend == True:
        p1.addLegend()

    return p1

def update_freq_plot(audio_object, plot, colour, add_legend=False):
    x = audio_object.fft_freqs
    channel_counter = 0
    for i in audio_object.fft_db:
        y = i
        if add_legend == True:
            if len(audio_object.fft_db) == 1:
                plot.plot(x=x, y=y, pen=colour, name=audio_object.name)
            else:
                plot.plot(x=x, y=y, pen=colour, name=audio_object.name+str(channel_counter))
                channel_counter += 1
        else:
            plot.plot(x=x, y=y, pen=colour)


def add_time_plot(window, row, col, legend=False):
    p2 = window.addPlot(row=row,col=col)
    p2.showGrid(x=True, y=True, alpha=100)   # To show grid lines across x axis and y axis
    bottomaxis = p2.getAxis('bottom')
    bottomaxis.setLogMode(False)
    p2.setLabel(axis='bottom', text='Time', units='Secs')
    p2.setLabel(axis='left', text='Level')
    p2.showGrid(x=True,y=True)
    if legend == True:
        p2.addLegend()
    return p2

def update_time_plot(audio_object, plot, colour, add_legend=False):
    x = audio_object.time_axis
    channel_counter = 0
    for i in audio_object.signal:
        y = i
        if add_legend == True:
            if len(audio_object.signal) == 1:
                plot.plot(x=x, y=y, pen=colour, name=audio_object.name)
            else:
                plot.plot(x=x, y=y, pen=colour, name=audio_object.name+str(channel_counter))
                channel_counter += 1
        else:
            plot.plot(x=x, y=y, pen=colour)

def update_time_envelope_plot(audio_object, plot, colour,add_legend=False):
    try:
        x = audio_object.env_time
        channel_counter = 0
        for i in audio_object.env_amplitude:
            y = i
            if add_legend == True:
                if len(audio_object.env_amplitude) == 1:
                    plot.plot(x=x, y=y, pen=colour, name=audio_object.name+" Envelope")
                else:
                    plot.plot(x=x, y=y, pen=colour, name=audio_object.name+str(channel_counter)+ " Envelope")
                    channel_counter += 1
            else:
                plot.plot(x=x, y=y, pen=colour)
    except Exception as e:
        print(f"Envelope plotting failed: {e}")

def add_label(window, value, justify):
    label = pg.LabelItem(justify=justify)
    label.setText(value)
    window.addItem(label)



