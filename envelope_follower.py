#import librosa
#import librosa.display
from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
#import IPython.display as ipd

#class EnvelopeFollower():

audio_file = "4AM_2.wav"
FRAME_SIZE = 1024
HOP_LENGTH = int(FRAME_SIZE / 2)

#ipd.Audio(audio_file)
sr, audio_data = wavfile.read(audio_file)
no_samples = len(audio_data)

sample_duration = 1 / sr
print(f"Duration of 1 sample is {sample_duration:.6f} seconds")
sample_time = np.arange(0,no_samples)
sample_time = sample_time * sample_duration
# Duration of audio signal in seconds

duration = sample_duration * no_samples
print(f"Duration of signal is {duration:.2f} seconds")

# Calculate the amplitude envelope

def amplitude_envelope(signal, frame_size, hop_length, sr):
    amplitude_envelope = []

    # Calculate amplitiude envelope for each frame

    for i in range(0, len(signal), hop_length):
        current_frame_ae = max(signal[i:i+frame_size])
        amplitude_envelope.append(current_frame_ae)
    
    frames = range(0,len(amplitude_envelope))
    times=[]
    for i in frames:
        times.append(i * hop_length/sr)

    return np.array(amplitude_envelope), times

def fancy_amplitude_envelope(signal, frame_size, hop_length):
    return np.array([max(signal[i:i+frame_size]) for i in range(0,len(signal), hop_length)])

ae_audio, times = amplitude_envelope(audio_data, FRAME_SIZE, HOP_LENGTH, sr)
print(len(ae_audio))

# Visualise amplitude envelope 

# Visualise the waveforms


#plt.figure(figsize=(15, 17))
plt.title("4AM")
plt.ylim((-2,2))
plt.plot(sample_time,audio_data / 2**15)
plt.plot(times, ae_audio/2**15, color="r")
plt.show()
print("done")

