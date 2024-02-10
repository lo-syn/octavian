from scipy.io import wavfile
import numpy as np
import os

class AudioFile(object):

    '''
    Reads a .wav audio file and returns it as an Object
    This is mainly just to allow all processing functions to work

    Parameters
    ----------
    file_path : str
        Path for file

    Returns
    -------
    file : AudioFile.signal
        Returns a list of arrays with audio file signal

    time_axis : AudioFile.time_axis
        Returns a 1D array with the time axis

    Examples
    --------
    >>> audio_file = AudioFile(file_path)

    .. plot::

        import matplotlib.pyplot as plt
        from audiofile import AudioFile

        audiofile = AudioFile(file_path)
        colour_list=['r','b','g'] # Will only work for 3 arrays because I'm lazy
        for i in range(len(audiofile.signal)):
            plt.plot(audiofile.time_axis, audiofile.signal[i], color=colour_list[i])
        plt.title('Audio File')
        plt.ylabel('Amplitude')
        plt.ylim([-1, 1])
        plt.xlabel('Time (secs)')
        plt.show()
    '''

    def __init__(self, 
                file_path: str,
                ):
        AudioFile._check_parameters(file_path)
        self.file_path = file_path
        self.run()
    
    def open_audiofile(self):
        '''
        This function opens audio file
        '''
        self.samplerate, signal = wavfile.read(self.file_path)
        self.num_channels = signal.shape  
        convert_16bit = float(2**15)
        signal_list = []
        signal = np.transpose(signal)
        if signal.size > 1:
            for i in signal:
                signal_list.append(i/ (convert_16bit))
        self.signal = signal_list
        step = 1 / self.samplerate
        time_axis = np.arange(0,len(self.signal[0]))
        self.time_axis = time_axis * step
        self.name = os.path.basename(self.file_path)

    def run(self):
        self.open_audiofile()
        
    @staticmethod
    def _check_parameters(file_path):
        """Checks the parameters for audio file, raises exceptions if necessary."""
        pass # Should add a check that file path exists here