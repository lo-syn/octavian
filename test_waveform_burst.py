from sine_burst import SineBurst

def test_inputs():
    pass

import matplotlib.pyplot as plt
from sine_burst import SineBurst
sine_burst = SineBurst(1000, -3, 0.1, 48000, windowed=True)
plt.plot(sine_burst.time_axis,sine_burst.signal)
plt.title('Sine Burst')
plt.ylabel('Amplitude')
plt.ylim([-1, 1])
plt.xlabel('Time (secs)')
plt.show()
print("pause")