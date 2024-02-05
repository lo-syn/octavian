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