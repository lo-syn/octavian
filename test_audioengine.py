from pyaudioengine import AudioStreamer



audio_streamer = AudioStreamer(
    'Primary Sound Driver')

audio_streamer.initialize_output_device()
audio_streamer.initialise_stream()
audio_stream = audio_streamer.stream_instance
print(f"Initialised {audio_stream}")