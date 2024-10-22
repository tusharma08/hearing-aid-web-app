import numpy as np
from scipy.signal import butter, lfilter

SAMPLE_RATE = 44100  # Sample rate in Hz

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

def bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def process_audio_data(audio_data, amplification_factor, noise_reduction_level):
    # Amplify the audio signal
    amplified_data = audio_data * amplification_factor

    # Band-pass filter for isolating speech frequencies (300Hz to 3400Hz)
    filtered_data = bandpass_filter(amplified_data, lowcut=300, highcut=3400, fs=SAMPLE_RATE)

    # Apply noise reduction (low-pass filter) only if noise reduction level > 0
    if noise_reduction_level > 0:
        cutoff_freq = max((1.0 - (noise_reduction_level / 100.0)) * SAMPLE_RATE // 2, 50)
        filtered_data = lowpass_filter(filtered_data, cutoff=cutoff_freq, fs=SAMPLE_RATE)

    # Clip the data to avoid overflow
    filtered_data = np.clip(filtered_data, -32768, 32767)
    
    return filtered_data.astype(np.int16)

# Simple low-pass filter for general noise reduction
def butter_lowpass(cutoff, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y
