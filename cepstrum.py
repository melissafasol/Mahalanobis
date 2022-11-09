import os 
import numpy as np 
import pandas as pd


def compute_cepstrum(signal, sample_freq):
    """Computes cepstrum."""
    frame_size = signal.size
    windowed_signal = np.hamming(frame_size) * signal
    dt = 1/sample_freq
    freq_vector = np.fft.rfftfreq(frame_size, d=dt)
    X = np.fft.rfft(windowed_signal)
    log_X = np.log(np.abs(X))
    cepstrum = np.fft.rfft(log_X)
    df = freq_vector[1] - freq_vector[0]
    quefrency_vector = np.fft.rfftfreq(log_X.size, df)
    return quefrency_vector, cepstrum

def cepstrum_f0_detection(signal, sample_freq, fmin=82, fmax=640):
    """Returns f0 based on cepstral processing."""
    quefrency_vector, cepstrum = compute_cepstrum(signal, sample_freq)
    # extract peak in cepstrum in valid region
    valid = (quefrency_vector > 1/fmax) & (quefrency_vector <= 1/fmin)
    max_quefrency_index = np.argmax(np.abs(cepstrum)[valid])
    f0 = 1/quefrency_vector[valid][max_quefrency_index]
    return f0