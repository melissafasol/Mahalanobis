import os 
import numpy as np 
import pandas as pd


def compute_cepstrum(signal, freq_vector, sample_freq, spectrogram):
    """Computes cepstrum."""
    if spectrogram == True:
        frame_size = signal.size
        df = freq_vector[1] - freq_vector[0]
        log_X = np.log(np.abs(signal))
        cepstrum = (np.fft.ifft(log_X)).real
        quefrency_vector = np.fft.fftfreq(cepstrum.size, df)
    else:
        frame_size = signal.size
        windowed_signal = np.hamming(frame_size) * signal
        dt = 1/sample_freq
        freq_vector = np.fft.fftfreq(frame_size, d=dt)
        X = np.fft.fft(windowed_signal)
        log_X = np.log(np.abs(X))
        cepstrum = np.fft.ifft(log_X)
        df = freq_vector[1] - freq_vector[0]
        quefrency_vector = np.fft.fftfreq(log_X.size, df)
    return quefrency_vector, cepstrum

def cepstrum_f0_detection(quefrency_vector, cepstrum, fmin=2, fmax=30):
    """Returns f0 based on cepstral processing."""
    # extract peak in cepstrum in valid region
    valid = (quefrency_vector > 1/fmax) & (quefrency_vector <= 1/fmin)
    max_quefrency_index = np.argmax(np.abs(cepstrum)[valid])
    f0 = 1/quefrency_vector[valid][max_quefrency_index]
    return f0