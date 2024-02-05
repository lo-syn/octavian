from sine_burst import SineBurst

def test_inputs():
    pass

import matplotlib.pyplot as plt
from sine_burst import SineBurst
sine_burst = SineBurst(1000, -3, 1, 48000, windowed=False)
windowed_sine_burst = SineBurst(1000, -3, 1, 48000, windowed=True)
plt.plot(sine_burst.time_axis, sine_burst.signal, color='r')
plt.plot(windowed_sine_burst.time_axis, windowed_sine_burst.signal, color='b')
plt.title('Sine Bursts')
plt.ylabel('Amplitude')
plt.ylim([-1, 1])
plt.xlabel('Time (secs)')
plt.show()
print("pause")