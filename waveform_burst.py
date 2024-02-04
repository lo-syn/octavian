

class WaveformBurst(object):

    def __init__(self, 
                freq: int,
                lin_amplitude: float,
                duration: float,
                samplerate: int
                ):
        WaveformBurst._check_parameters(freq,lin_amplitude,duration,samplerate)
        self.freq = freq
        self.lin_amplitude = lin_amplitude
        self.duration = duration
        self.samplerate = samplerate
    
    @staticmethod
    def _check_parameters(freq, lin_amplitude, duration, samplerate):
        """Checks the parameters for a synchronized sweep, raises exceptions if neccessary."""
        if freq <= 0:
            raise ValueError(
                f'`Freq` (={freq}) must be bigger than 0.')
        if duration <= 0:
            raise ValueError(f'`Duration` ({duration}) must be bigger than 0.')
        if lin_amplitude <= 0 or lin_amplitude > 1:
            raise ValueError(f'`Amplitude` ({lin_amplitude}) is outside of usuable range (0-1).')
        if samplerate <= 0:
            raise ValueError('Sample Rate must be bigger than 0.')
        if samplerate < 2*freq:
            raise ValueError(
                '`Sample Rate` must be at least twice `Freq`')

    #@property
    #def freq(self) -> int:
    #    return self._freq
        
x = WaveformBurst(1000,1,1,48000)
print(x.freq)


    
