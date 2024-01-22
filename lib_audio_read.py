# import scipy

# def audio_file_read(filename):
#     audio_data = scipy.io.wavfile.read(filename)
#     return audio_data

import wave

def audio_file_read(filename):
    audio_data = wave.open(filename, "r")
    num_channels = int(audio_data.getnchannels())

    return num_channels