import matplotlib.pyplot as plt
from audiofile import AudioFile
file_path = r"C:\Users\laure\OneDrive\Documents\Octavian\4AM.wav"

audiofile = AudioFile(file_path)
colour_list=['r','b','g']
for i in range(len(audiofile.signal)):
    plt.plot(audiofile.time_axis, audiofile.signal[i], color=colour_list[i])
plt.title('Audio File')
plt.ylabel('Amplitude')
plt.ylim([-1, 1])
plt.xlabel('Time (secs)')
plt.show()