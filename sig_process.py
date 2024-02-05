

def audio_slicer(audio_object, start_secs, end_secs, fs):
    start_sample = int(start_secs * fs)
    end_sample = int(end_secs * fs)
    audio_object.signal = audio_object.signal[start_sample:end_sample]
    audio_object.time_axis = audio_object.time_axis[start_sample:end_sample]

    return audio_object