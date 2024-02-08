import sounddevice as sd
import soundfile as sf
import numpy as np
import time

AUDIO_SAMPLE_RATE = 48000

audio_devices = sd.query_devices()
audio_host_api = sd.query_hostapis()

for i in range(len(audio_host_api)):
    if audio_host_api[i]["name"] == "ASIO":
        asio_device_ids = audio_host_api[i]
        asio_devices = []
        for device_id in asio_device_ids["devices"]:
            asio_devices.append(audio_devices[device_id])

fs_stream = asio_devices[1]["default_samplerate"]

sd.default.samplerate = asio_devices[1]["default_samplerate"]
sd.default.device = asio_devices[1]["index"]
print(sd.check_output_settings(sd.default.device))

x, fs = sf.read('5s_-4_2dbfs.wav')

#if int(fs) != int(AUDIO_SAMPLE_RATE):
    #print("Sample rate mismatch: File vs Constant")

#if int(fs) != fs_stream:
    #print("Sample rate mismatch: File vs Stream")

x = np.float32(x)

asio_stream = sd.Stream(
                samplerate=fs_stream,
                device=asio_devices[1]["index"],
                channels=30,
                )
asio_stream.start()
if asio_stream.active:
    print("ASIO Audio Stream running")
asio_stream.write(x)
asio_stream.stop()
time.sleep(20)