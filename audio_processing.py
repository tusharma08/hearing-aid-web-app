import numpy as np
from scipy.signal import butter, lfilter

SAMPLE_RATE = 44100  # Sample rate in Hz

def butter_lowpass(cutoff, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

def process_audio_data(audio_data, amplification_factor, noise_reduction_level):
    amplified_data = audio_data * amplification_factor

    if noise_reduction_level > 0:
        cutoff_freq = max((1.0 - (noise_reduction_level / 100.0)) * SAMPLE_RATE // 2, 50)
        amplified_data = lowpass_filter(amplified_data, cutoff=cutoff_freq, fs=SAMPLE_RATE)

    amplified_data = np.clip(amplified_data, -32768, 32767)
    return amplified_data.astype(np.int16)
