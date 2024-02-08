from pyaudioengine import AudioStreamer
from sounddevice_engine import SdAudioStreamer


audio_streamer = AudioStreamer(
    'Primary Sound Driver')

sd_audio_streamer = SdAudioStreamer('Primary Sound Driver')

audio_streamer.initialize_output_device()
sd_audio_streamer.initialize_output_device()
audio_streamer.initialise_stream()
audio_stream = audio_streamer.stream_instance
print(f"Initialised {audio_stream}")