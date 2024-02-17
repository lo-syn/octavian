from sounddevice_engine import SdAudioStreamer
from sine_burst import SineBurst

import numpy as np

def callback(indata, outdata, frames, time, status):
    if status:
        print(status)
    data = np.array(sine_burst.signal)[
            frames * cb_count : frames * (cb_count + 1)
        ]
    cb_count = cb_count + 1
    outdata[:] = data

sine_burst = SineBurst(1000,-24,1,48000)
sd_audio_streamer = SdAudioStreamer(output_device='Primary Sound Driver')

sd_audio_streamer.initialize_output_device()
sd_audio_streamer.initialise_stream()
audio_stream = sd_audio_streamer.stream_instance
print(f"Initialised {audio_stream}")
print(audio_stream.active)

import sounddevice as sd
duration = 5.5  # seconds

cb_count = 0

with sd.Stream(channels=2, callback=callback):
    sd.sleep(int(duration * 1000))

sd_audio_streamer.play_sd_stream(np.array(sine_burst.signal),2)
#audio_stream.write(np.ascontiguousarray(sine_burst.signal.as type(np.float32)))