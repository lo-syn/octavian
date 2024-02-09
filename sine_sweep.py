import math
import numpy as np

class SineSweep(object):

    '''
    Generates an  sine sweep of various waveform shapes (sine, square, triangle, saw)

    Parameters
    ----------
    freq1 : scalar
        Start frequency of sweep in Hz
    freq2 : scalar
        Stop frequency of sweep in Hz
    db_amplitude : scalar
        Logarithmic amplitude of burst, with range -120 to 0 (dBFS) 
    duration_s : scalar
        Duration in seconds
    samplerate : scalar
        Samplerate of the signal in Hz.

    Returns
    -------
    sweep : SineBurst.signal
        Returns a 1D array with sine sweep signal

    time_axis : SineBurst.time
        Returns a 1D array with the time axis

    Examples
    --------
    >>> sine_sweep = SineSweep(20, 20000, -3, 1, 48000)

    .. plot::

        import matplotlib.pyplot as plt
        from sine_sweep import SineSweep
        sine_sweep = SineSweep(20,200, -3, 1, 48000, windowed=False)
        windowed_sine_sweep = SineSweep(20, 200, -12, 1, 48000, windowed=True)
        plt.plot(sine_sweep.time_axis, sine_sweep.signal, color='r')
        plt.plot(windowed_sine_sweep.time_axis, windowed_sine_sweep.signal, color='b')
        plt.title('Sine Bursts')
        plt.ylabel('Amplitude')
        plt.ylim([-1, 1])
        plt.xlabel('Time (secs)')
        plt.show()

    '''

    def __init__(self, 
                freq1: int,
                freq2: int,
                db_amplitude: float,
                duration_s: float,
                samplerate: int,
                windowed=None
                ):
        SineSweep._check_parameters(freq1,freq2,db_amplitude,duration_s,samplerate)
        self.freq1 = freq1
        self.freq2 = freq2
        self.db_amplitude = db_amplitude
        self.duration_s = duration_s
        self.samplerate = samplerate
        if windowed == True:
            self.windowed = windowed
        else:
            self.windowed = None
        self.run()
    
    def gen_sinesweep(self):
        '''
        This function generates an exponential sine sweep
        It is a Python implementation of the Matlab code found in Synchronized Sine Sweep paper
        '''
        startfreq = self.freq1
        stopfreq = self.freq2
        durationappr = self.duration_s
        samplerate = self.samplerate
    
        logfreqratio = np.log(stopfreq/startfreq)  # ln(f2/f1)

        # symbol $k$, eq. 32 from paper
        kappa = np.round(startfreq*durationappr/logfreqratio)

        # symbol $T$ in paper
        duration = kappa * logfreqratio / startfreq

        # symbol L in paper
        sweepperiod = kappa / startfreq
        dt = 1.0 / samplerate
        time = np.arange(0, duration, dt)
        # eq. 33 from paper
        phi = 2*np.pi*startfreq*sweepperiod*np.exp(time/sweepperiod)
        sweep = np.sin(phi)

        # keep as private attributes
        self._logfreqratio = logfreqratio
        self._kappa = kappa

        gain_dbfs = 10 ** (self.db_amplitude/20)
        sweep = sweep * gain_dbfs

        # make accessible through readonly properties
        self._sweepperiod = sweepperiod
        self._duration = duration
        self.time_axis = time
        self.signal = [sweep]

    def windowing(self, sine_sweep):
        '''
        This method applies a cosine window to the first 
        '''
        fade_samples = int(len(sine_sweep) / 10)
        fade = np.arange(0, fade_samples-1, dtype=int)
        fade_in = (1 - np.cos(fade/fade_samples*math.pi))/2
        fade_out = np.flip(fade_in)
        idx = np.arange(1,fade_samples)
        sine_sweep[idx]=sine_sweep[idx] * fade_in
        sine_sweep[-len(idx)::]=sine_sweep[-len(idx)::] * fade_out
        self.signal = sine_sweep

    def run(self):
        self.gen_sinesweep()
        if self.windowed == True:
            self.windowing(self.signal)
    
    @staticmethod
    def _check_parameters(freq1, freq2, db_amplitude, duration_s, samplerate):
        """Checks the parameters for a synchronized sweep, raises exceptions if necessary."""
        if freq1 <= 0:
            raise ValueError(
                f'`Freq1` (={freq1}) must be bigger than 0.')
        if freq2 <= 0:
            raise ValueError(
                f'`Freq2` (={freq2}) must be bigger than 0.')
        if duration_s <= 0:
            raise ValueError(f'`Duration` ({duration_s}) must be bigger than 0.')
        if db_amplitude < -120 or db_amplitude > 0:
            raise ValueError(f'`Amplitude` ({db_amplitude}) is outside of usuable range (-120 -> 0).')
        if samplerate <= 0:
            raise ValueError('Sample Rate must be bigger than 0.')
        if samplerate < 2*freq2:
            raise ValueError(
                '`Sample Rate` must be at least twice `Freq2`')
        if freq1 > freq2:
            raise ValueError(
                '`Freq2` is greater than `Freq1`'
            )
