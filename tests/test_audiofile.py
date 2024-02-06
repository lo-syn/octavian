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