from scipy.io import wavfile
import numpy as np

class AudioFile(object):

    """
    Reads a .wav audio file and returns it as an Object
    This is mainly just to allow all processing functions to work

    Parameters
    ----------
    file_path : str
        Path for file

    Returns
    -------
    file : AudioFile.signal
    time_axis : AudioFile.time_axis

    Examples
    --------
    >>> audio_file = AudioFile("test.wav")

    .. plot::

        import matplotlib.pyplot as plt
        from audiofile import AudioFile
        audiofile = AudioFile(r"C:\Users\laure\OneDrive\Documents\Octavian\4AM.wav")
        print(audiofile.signal)
        plt.plot(audiofile.time_axis, audiofile.signal, color='r')
        plt.title('Audio File')
        plt.ylabel('Amplitude')
        plt.ylim([-1, 1])
        plt.xlabel('Time (secs)')
        plt.show()
    """

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
        self.num_channels = int(self.signal.getnchannels())
        convert_16bit = float(2**15)
        self.signal = (signal / (convert_16bit))
        step = 1 / self.samplerate
        time_axis = np.arange(0,len(self.signal))
        self.time_axis = time_axis * step

    def run(self):
        self.open_audiofile()
        

    
    @staticmethod
    def _check_parameters(file_path):
        """Checks the parameters for noise, raises exceptions if necessary."""
        pass # Should add a check that file path exists here