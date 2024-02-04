import numpy as np
from math import pi

class SineBurst(object):

    '''
    Generates a tone burst of various waveform shapes (sine, square, triangle, saw)

    Parameters
    ----------
    freq : scalar
        Frequency of tone burst in Hz
    db_amplitude : scalar
        Logarithmic amplitude of burst, with range -120 to 0 (dBFS) 
    duration_s : scalar
        Duration in seconds
    samplerate : scalar
        Samplerate of the signal in Hz.

    Returns
    -------
    signal : SineBurst.signal
    time_axis : SineBurst.time

    Examples
    --------
    >>> sweep = SineBurst(1000, -3, 1, 48000)

    .. plot::

        import matplotlib.pyplot as plt
        from sine_burst import SineBurst
        sine_burst = SineBurst(1000, -3, 0.1, 48000, windowed=False)
        windowed_sine_burst = SineBurst(1000, -3, 0.1, 48000, windowed=True)
        plt.plot(sine_burst.time_axis,sine_burst.signal)
        plt.plot(windowed_sine_burst.time_axis, windowed_sine_burst.signal)
        plt.title('Sine Bursts')
        plt.ylabel('Amplitude')
        plt.ylim([-1, 1])
        plt.xlabel('Time (secs)')
        plt.show()

    '''

    def __init__(self, 
                freq: int,
                db_amplitude: float,
                duration_s: float,
                samplerate: int,
                windowed=None
                ):
        SineBurst._check_parameters(freq,db_amplitude,duration_s,samplerate)
        self.freq = freq
        self.db_amplitude = db_amplitude
        self.duration_s = duration_s
        self.samplerate = samplerate
        if windowed == True:
            self.windowed = windowed
        else:
            self.windowed = None
        self.run()
    
    def gen_sineburst(self):
        '''
        This method generates the sine burst
        '''
        length = np.pi * 2 * self.freq
        gain_dbfs = 10 ** (self.db_amplitude/20)
        sine_burst = gain_dbfs * np.sin(
            np.arange(0, length * self.duration_s, length / self.samplerate)
        )
        step = 1 / self.samplerate
        time_axis = np.arange(0,len(sine_burst))
        self.time_axis = time_axis * step
        self.signal = sine_burst

        return sine_burst

    def windowing(self, sine_burst):
        '''
        This method applies a cosine window to the first 
        '''
        fade_samples = int(len(sine_burst) / 10)
        fade = np.arange(0, fade_samples-1, dtype=int)
        fade_in = (1 - np.cos(fade/fade_samples*pi))/2
        fade_out = np.flip(fade_in)
        idx = np.arange(1,fade_samples)
        sine_burst[idx]=sine_burst[idx] * fade_in
        sine_burst[-len(idx)::]=sine_burst[-len(idx)::] * fade_out
        self.signal = sine_burst

    def run(self):
        sine_burst = self.gen_sineburst()
        if self.windowed == True:
            self.windowing(sine_burst)
    
    @staticmethod
    def _check_parameters(freq, db_amplitude, duration, samplerate):
        """Checks the parameters for a synchronized sweep, raises exceptions if neccessary."""
        if freq <= 0:
            raise ValueError(
                f'`Freq` (={freq}) must be bigger than 0.')
        if duration <= 0:
            raise ValueError(f'`Duration` ({duration}) must be bigger than 0.')
        if db_amplitude < -120 or db_amplitude > 0:
            raise ValueError(f'`Amplitude` ({db_amplitude}) is outside of usuable range (-120 -> 0).')
        if samplerate <= 0:
            raise ValueError('Sample Rate must be bigger than 0.')
        if samplerate < 2*freq:
            raise ValueError(
                '`Sample Rate` must be at least twice `Freq`')


    
