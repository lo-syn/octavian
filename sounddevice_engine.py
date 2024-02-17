import itertools
import time
from typing import Any

import numpy as np
import pyaudio
import scipy.io.wavfile as wf
from pynput.keyboard import Controller, Key
import sounddevice as sd


AUDIO_BUFFER_SIZE = 2048
AUDIO_SAMPLING_RATE = 48000
HOST_API_INDEX = 1
AUDIO_FORMAT = pyaudio.paInt32


def turn_up_volume() -> None:
    """
    Turn up OS master volume
    """
    keyboard = Controller()
    for i in range(50):
        keyboard.press(Key.media_volume_up)
        keyboard.release(Key.media_volume_up)

def reset_volume() -> None:
    """
    Reset OS master volume to 50%
    """
    keyboard = Controller()
    for i in range(50):
        keyboard.press(Key.media_volume_down)
        keyboard.release(Key.media_volume_down)
    for i in range(25):
        keyboard.press(Key.media_volume_up)
        keyboard.release(Key.media_volume_up)


class SdAudioStreamer:
    def __init__(self, output_device: str, input_device: str | None = None) -> None:
        self.output_devices: list[dict[str, Any]] = []
        self.input_devices: list[dict[str, Any]] = []
        self.output_device_name = output_device
        self.input_device_name = input_device
        self.device_index: int | None = None
        self.input_device_index = None
        self.input_device_no_of_channels = None
        self.stream = None

    def initialize_output_device(self) -> None:
        """
        Check if the right audio output device is selected in the OS
        """
        # Search for output device
        devices = sd.query_devices()
        found_output_device = False
        for i in devices:
            if self.output_device_name in i["name"]:
                print(f"Found device '{self.output_device_name}' with idx {i['index']} ")
                found_output_device = True
                self.output_device_index = i["index"]
                self.output_device_no_of_channels = i["max_output_channels"]
        if found_output_device != True:
            print(f"Unable to find output device: {self.output_device_name}")



#        device_index = -1
#        for i in range(0, device_count):
#            if (
#                sd.query_hostapis(HOST_API_INDEX, i).get(
#                    "maxOutputChannels"
#                )
#            ) > 0:
#                device_name = sd.query_hostapis(
#                    HOST_API_INDEX, i
#                ).get("name")
#                self.output_devices.append({"name": device_name, "index": i})
#        for device in self.output_devices:
#            if device["name"] == self.output_device_name:
#                device_index = device["index"]
#                break
#        if device_index == -1:
#            raise Exception(
#                'Audio output device "{}" could not be found.'.format(
#                    self.output_device_name
#                )
#            )


        # Check if output device is selected in the OS
        # current_default_output = self.pa.get_default_output_device_info()
        # if current_default_output["name"] != self.output_device_name:
        #     raise Exception(
        #         f'Audio output device "{self.output_device_name}" is not selected in the OS.'
        #     )
        # turn_up_volume()

    def initialize_input_device(self) -> None:
        """
        Check if the right audio output device is selected in the OS
        """
        # Search for output device
        # Search for output device
        devices = sd.query_devices()
        found_input_device = False
        for i in devices:
            if self.input_device_name in i["name"]:
                print(f"Found device '{self.input_device_name}' with idx {i['index']} ")
                found_input_device = True
                self.input_device_index = i["index"]
                self.input_device_no_of_channels = i["max_input_channels"]
        if found_input_device != True:
            print(f"Unable to find input device: {self.input_device_name}")

    def play_stream(
        self, content: str | np.ndarray, channel: int | None = None
    ) -> tuple[np.ndarray | None, np.ndarray]:
        self.content = None
        if isinstance(content, str):
            sampling_rate, data = wf.read(content)
            if channel is not None:
                self.content = data[:, channel]
            else:
                self.content = data[:]
            self.content = self.content.copy(order="C")
        elif isinstance(content, np.ndarray):
            self.content = content
            sampling_rate = AUDIO_SAMPLING_RATE

        self.cb_count = 0
        enable_recording = True if self.input_device_name is not None else False

        stream = self.pa.open(
            format=AUDIO_FORMAT,
            channels=1,
            rate=sampling_rate,
            output=True,
            output_device_index=self.device_index,
            input=enable_recording,
            input_device_index=self.input_device_index,
            start=False,
            stream_callback=self.callback,
            frames_per_buffer=AUDIO_BUFFER_SIZE,
        )

        recorded_frames = []
        # Start stream
        stream.start_stream()

        # Wait for stream to finish
        while stream.is_active():
            time.sleep(0.2)

        # Stop the stream
        if stream.is_active():
            stream.stop_stream()
        stream.close()

        # Process input data
        audio_output_data = self.content

        # Process recorded data
        if self.input_device_name is not None:
            input_channels = int(
                self.pa.get_device_info_by_host_api_device_index(
                    HOST_API_INDEX, self.input_device_index
                ).get("maxInputChannels")
            )
            if input_channels > 1:
                frames_count = AUDIO_BUFFER_SIZE * input_channels
            else:
                frames_count = AUDIO_BUFFER_SIZE
            audio_data = []
            for i in self.recorded_frames:
                chunk_as_int16_data = np.frombuffer(
                    i, dtype=np.int16, count=frames_count
                )
                if input_channels > 1:
                    audio_data.append(
                        chunk_as_int16_data[::2]
                    )  # chunk_as_int16_data[1::2] for second channel
                else:
                    audio_data.append(chunk_as_int16_data)
            result = list(itertools.chain.from_iterable(audio_data))
            audio_input_data = np.array(result)
            return audio_input_data, audio_output_data
        else:
            return None, audio_output_data

    def initialise_stream(self, channel: int | None = None
    ) -> tuple[np.ndarray | None, np.ndarray]:
        self.content = []
        self.cb_count = 0
        enable_recording = True if self.input_device_name is not None else False

        stream = sd.Stream(
            device=self.output_device_name,
            blocksize=1024,
            channels=1, # This should be multichannel compatible
            dtype= 'int16',
            samplerate=AUDIO_SAMPLING_RATE,
            callback=self.callback,
        )
        stream.start()
        self.stream_instance = stream

    def write(self, data):
        self.stream_instance.write(data)





    def play_stream_non_blocking(
        self, content: str | np.ndarray, channel: int | None = None
    ) -> tuple[np.ndarray | None, np.ndarray]:
        self.content = None
        if isinstance(content, str):
            sampling_rate, data = wf.read(content)
            if channel is not None:
                self.content = data[:, channel]
            else:
                self.content = data[:]
            self.content = self.content.copy(order="C")
        elif isinstance(content, np.ndarray):
            self.content = content
            sampling_rate = AUDIO_SAMPLING_RATE

        audio_format: int = {
            np.dtype("int8"): pyaudio.paInt8,
            np.dtype("int16"): pyaudio.paInt16,
            np.dtype("int32"): pyaudio.paInt32,
        }.get(self.content.dtype)
        self.cb_count = 0
        enable_recording = True if self.input_device_name is not None else False

        self.stream = self.pa.open(
            format=audio_format,
            channels=1,
            rate=sampling_rate,
            output=True,
            output_device_index=self.device_index,
            input=enable_recording,
            input_device_index=self.input_device_index,
            start=False,
            stream_callback=self.callback,
            frames_per_buffer=AUDIO_BUFFER_SIZE,
        )

        self.recorded_frames = []
        # Start stream
        self.stream.start_stream()

    def play_sd_stream(
        self, content: str | np.ndarray, channel: int | None = None
    ) -> tuple[np.ndarray | None, np.ndarray]:
        self.content = content
        if isinstance(content, str):
            sampling_rate, data = wf.read(content)
            if channel is not None:
                self.content = data[:, channel]
            else:
                self.content = data[:]
            self.content = self.content.copy(order="C")
        elif isinstance(content, np.ndarray):
            self.content = content
            sampling_rate = AUDIO_SAMPLING_RATE

        audio_format: int = {
            np.dtype("int8"): pyaudio.paInt8,
            np.dtype("int16"): pyaudio.paInt16,
            np.dtype("int32"): pyaudio.paInt32,
        }.get(self.content.dtype)
        self.cb_count = 0

        ''' Write stream functionality here '''

        self.stream_instance.write(self.content)        

    def stop_stream(self) -> None:
        if self.stream.is_active():
            self.stream.stop_stream()
        self.stream.close()
        self.stream = None

    def callback(
        self, indata: Any, outdata: Any, frames: Any, time: Any, status: Any
    ) -> None:
        data = self.content[
            frames * self.cb_count : frames * (self.cb_count + 1)
        ]
        self.cb_count = self.cb_count + 1
#
        if self.input_device_name is not None:
            self.recorded_frames.append(indata)
        return (data)#, pyaudio.paContinue)

    def close(self) -> None:
        self.pa.terminate()