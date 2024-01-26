from scipy.io import wavfile
import scipy.io
import numpy as np
import matplotlib.pyplot as plt

from lib_sig_process import audio_slicer


filename = r"C:\Users\laurence.porter\Documents\Test_Development\Octavian\Driver1_Imp_V_-6dBFS.wav"
SCALE_V = 11 / (2**15)
SCALE_I = 3 / (2**15)

samplerate, data = wavfile.read(filename)
#print(f"number of channels = {data.shape[1]}")

start_time = 0.5720
burst_length = 5

data = audio_slicer(data, start_time,start_time+burst_length+0.002,samplerate)

length = data.shape[0] / samplerate

time = np.linspace(0., length, data.shape[0])

#driver_idx_to_VPB_channel = {1:7, 2:8, 3:6, 4:5, 5:4, 6:3, 7:2, 8:16, 9:14, 10:13, 11:12, 12:11, 13:10, 14:9, 15:1, 16:15, 17:22, 18:21, 19:20, 20:19, 21:18, 22:17, 23:23, 24:24, 25:30, 26:29, 27:28, 28:27, 29:26, 30:25}

convert_16bit = float(2**15)
export_data = []
export_data.append(time)

#for i in range(data.shape[1]):
for i in range(1):
    #print(driver_idx_to_VPB_channel[i])
    #plot_data = (data[:, i] / (convert_16bit))
    plot_data = (data / (convert_16bit))
    plot_data = list(plot_data * SCALE_V)
    #plot_data = list(plot_data * SCALE_I)
    export_data.append(plot_data)
    plt.plot(time, plot_data, label="VPB "+str(i))

export_data = np.array(export_data)
export_data = np.transpose(export_data)
np.savetxt("Burst.txt", export_data, delimiter=",")

plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.show()
print()