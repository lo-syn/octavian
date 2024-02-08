from pyaudioengine import AudioStreamer
from sounddevice_engine import SdAudioStreamer
from sine_burst import SineBurst

import numpy as np

sd_audio_streamer = SdAudioStreamer(output_device='Primary Sound Driver')
sine_burst = SineBurst(1000,-12,1,48000)

sd_audio_streamer.initialize_output_device()
sd_audio_streamer.initialise_stream()
audio_stream = sd_audio_streamer.stream_instance
print(f"Initialised {audio_stream}")
print(audio_stream.active)
#while audio_stream.stream_instance:
audio_stream.write(np.ascontiguousarray(sine_burst.signal.astype(np.float32)))