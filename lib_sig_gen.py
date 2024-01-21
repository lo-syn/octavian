import numpy as np
import scipy

''' ALL SIGNAL GENERATION IS DONE AS FLOAT32 (conversion to int16 happens at end of signal chain)

    Audio is always generated as 2d array: 
    1st array = Time axis (secs)
    2nd array = Audio data (float32 data)
'''

''' Functions for signal generation '''

def time_axis_gen(audio_array, fs):
    step = 1 / fs
    time_axis = np.arange(0,len(audio_array))
    time_axis = time_axis * step

    return time_axis

# Sine wave

def sine_wave_gen(
    freq, fs, duration_secs, amplitude_dBFS
):
    # Returns float32 sine wave at specific frequency for specified duration and amplitude

    length = np.pi * 2 * freq
    gain_dbfs = 10 ** (amplitude_dBFS/20)
    tone_burst = gain_dbfs * np.sin(
        np.arange(0, length * duration_secs, length / fs)
    )
    time_axis = time_axis_gen(tone_burst,fs)
    tone_burst = np.stack((time_axis,tone_burst))

    return tone_burst

def sine_sweep_gen(fmin, fmax, fs, duration_secs, amplitude_dBFS):

    sample_array = np.linspace(
        0, duration_secs, fs * duration_secs, endpoint=False
    )  # Sample Array
    sweep = scipy.signal.chirp(
        sample_array, fmin, duration_secs, fmax, method="logarithmic", phi=-90
    )  # Logarithmic sine wave Sweep

    amplitude_multiplier = 10 ** (amplitude_dBFS / 20)
    sweep = amplitude_multiplier * sweep

    time_axis = time_axis_gen(sweep,fs)
    sweep = np.stack((time_axis,sweep))

    return sweep

# Noise

def noise_gen(fs, duration_secs, noise_type, amplitude_dBFS):
    num_samples = int(fs / duration_secs)
    mean = 0
    std = 1

    samples = np.random.normal(mean, std, size=num_samples)
    multiplier = 1 / max(samples)
    noise = samples * multiplier

    if noise_type == str("pink"):
        B = [0.049922035, -0.095993537, 0.050612699, -0.004408786]
        A = [1, -2.494956002, 2.017265875, -0.522189400]

        noise = scipy.signal.lfilter(B, A, noise)

        multiplier = 1 / max(noise)
        noise = noise * multiplier

    amplitude_multiplier = 10 ** ((amplitude_dBFS) / 20)
    noise = noise * amplitude_multiplier

    time_axis = time_axis_gen(noise,fs)
    noise = np.stack((time_axis,noise))

    return noise





