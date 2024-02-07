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

def add_freq_plot(audio_object, window):
    x = audio_object.fft_freqs
    y = audio_object.fft_db
    p1 = window.addPlot(row=0,col=0)
    p1.setLabel(axis='bottom', text='Frequency', units='Hz')
    p1.setLabel(axis='left', text='Level', units='dB')
    p1.showGrid(x=True, y=True)   # To show grid lines across x axis and y axis
    p1.setLogMode(True)
    #rms_text = pg.TextItem(str("RMS (db):"+str(rms)))
    #peak_text = pg.TextItem(str("Peak (db):"+str(peak)))
    #cf_text = pg.TextItem(str("Crest Factor (db):"+str(crest_factor)))
    #p1.addItem(rms_text)
    #p1.addItem(peak_text)
    #p1.addItem(cf_text)
    #rms_text.setPos(0,0)
    #peak_text.setPos(1,0)
    #cf_text.setPos(2,0)

    p1.plot(x=x, y=y, pen=1)


def add_time_plot(audio_object, window):
    x = audio_object.time_axis
    y = audio_object.signal
    p2 = window.addPlot(row=1,col=0)
    p2.showGrid(x=True, y=True, alpha=100)   # To show grid lines across x axis and y axis
    bottomaxis = p2.getAxis('bottom')
    bottomaxis.setLogMode(False)
    p2.setLabel(axis='bottom', text='Time', units='Secs')
    p2.setLabel(axis='left', text='Level')
    p2.showGrid(x=True,y=True)

    p2.plot(x=x, y=y, pen=1)


