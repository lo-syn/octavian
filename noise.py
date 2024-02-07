import numpy as np
from scipy.signal import lfilter

class Noise(object):

    '''
    Generates a noise burst, either White or Pink (filtered) noise

    Parameters
    ----------
    db_amplitude : scalar
        Logarithmic amplitude of burst, with range -120 to 0 (dBFS) 
    duration_s : scalar
        Duration in seconds
    samplerate : scalar
        Samplerate of the signal in Hz.
    pinking_filter: bool
        Applies a pinking filter (for pink noise) if True

    Returns
    -------
    noise : Noise.signal
        Returns a 1D array with noise signal

    time_axis : Noise.time_axis
        Returns a 1D array with the time axis

    Examples
    --------
    >>> white_noise = Noise(-3, 1, 48000, pinking_filter=True)

    .. plot::

        import matplotlib.pyplot as plt
        from noise import Noise
        white_noise = Noise(-3, 1, 48000, pinking_filter=False)
        pink_noise = Noise(-3, 1, 48000, pinking_filter=True)
        plt.plot(white_noise.time_axis, white_noise.signal, color='r')
        plt.plot(pink_noise.time_axis, pink_noise.signal, color='b')
        plt.title('Noise')
        plt.ylabel('Amplitude')
        plt.ylim([-1, 1])
        plt.xlabel('Time (secs)')
        plt.show()

    '''

    def __init__(self, 
                db_amplitude: float,
                duration_s: float,
                samplerate: int,
                pinking_filter=False
                ):
        Noise._check_parameters(db_amplitude,duration_s,samplerate,pinking_filter)
        self.db_amplitude = db_amplitude
        self.duration_s = duration_s
        self.samplerate = samplerate
        if pinking_filter == True:
            self.pinking_filter = pinking_filter
        else:
            self.pinking_filter = False
        self.run()
    
    def gen_noise(self):
        '''
        This function generates white noise
        '''
        num_samples = int(self.samplerate / self.duration_s)
        mean = 0
        std = 1

        samples = np.random.normal(mean, std, size=num_samples)
        multiplier = 1 / max(samples)
        noise = samples * multiplier

        gain_dbfs = 10 ** (self.db_amplitude/20)
        noise = noise * gain_dbfs
        step = 1 / self.samplerate
        time_axis = np.arange(0,len(noise))
        self.time_axis = time_axis * step
        self.signal = noise

        return noise

    def apply_pinking_filter(self,noise):
        B = [0.049922035, -0.095993537, 0.050612699, -0.004408786]
        A = [1, -2.494956002, 2.017265875, -0.522189400]

        noise = lfilter(B, A, noise)

        multiplier = 1 / max(noise)
        noise = noise * multiplier
        gain_dbfs = 10 ** (self.db_amplitude/20)
        noise = noise * gain_dbfs
        self.signal = noise

    def run(self):
        noise = self.gen_noise()
        if self.pinking_filter == True:
            self.apply_pinking_filter(noise)
    
    @staticmethod
    def _check_parameters(db_amplitude,duration_s,samplerate,pinking_filter):
        """Checks the parameters for noise, raises exceptions if necessary."""
        if duration_s <= 0:
            raise ValueError(f'`Duration` ({duration_s}) must be bigger than 0.')
        if db_amplitude < -120 or db_amplitude > 0:
            raise ValueError(f'`Amplitude` ({db_amplitude}) is outside of usuable range (-120 -> 0).')
        if samplerate <= 0:
            raise ValueError('Sample Rate must be bigger than 0.')

        if not isinstance(pinking_filter, bool):
            raise ValueError(
                '`Pinking Filter` needs to be True or False'
            )