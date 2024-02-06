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