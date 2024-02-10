import pyqtgraph as pg
import numpy as np
import sys
from PyQt5.QtWidgets import *

def init_plot():
    app = QApplication(sys.argv)  # Create QApplication ***
    return app

def exec_plot(app):
    app.exec_()

def create_window():
    window = pg.GraphicsLayoutWidget()
    window.setGeometry(100, 100, 1400, 900)
    window.show()
    return window

def add_freq_plot(window, row, col):
    p1 = window.addPlot(row=row,col=col)
    p1.setLabel(axis='bottom', text='Frequency', units='Hz')
    p1.setLabel(axis='left', text='Level', units='dB')
    p1.showGrid(x=True, y=True)   # To show grid lines across x axis and y axis
    p1.setLogMode(True)

    return p1

def update_freq_plot(audio_object, plot, colour):
    x = audio_object.fft_freqs
    for i in audio_object.fft_db:
        y = i
        plot.plot(x=x, y=y, pen=colour)


def add_time_plot(window, row, col):
    p2 = window.addPlot(row=row,col=col)
    p2.showGrid(x=True, y=True, alpha=100)   # To show grid lines across x axis and y axis
    bottomaxis = p2.getAxis('bottom')
    bottomaxis.setLogMode(False)
    p2.setLabel(axis='bottom', text='Time', units='Secs')
    p2.setLabel(axis='left', text='Level')
    p2.showGrid(x=True,y=True)

    return p2

def update_time_plot(audio_object, plot, colour):
    x = audio_object.time_axis
    for i in audio_object.signal:
        y = i
        plot.plot(x=x, y=y, pen=colour)

def update_time_envelope_plot(audio_object, plot, colour):
    try:
        x = audio_object.env_time
        for i in audio_object.env_amplitude:
            y = i
            plot.plot(x=x, y=y, pen=colour)
    except Exception as e:
        print(e)

def add_label(window, value, justify):
    label = pg.LabelItem(justify=justify)
    label.setText(value)
    window.addItem(label)



