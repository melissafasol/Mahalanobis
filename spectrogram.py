import os 
import numpy as np
from scipy import signal 
from scipy.fft import fftshift
from matplotlib import mlab
import matplotlib.pyplot as plt


def specgram2d(y, srate=44100, ax=None, title=None):
    if not ax:
        ax = plt.axes()
        ax.set_title(title, loc='center', wrap=True)
        spec, freqs, t, im = ax.specgram(y, Fs=fs, scale='dB', vmax=0)
        ax.set_xlabel('time (s)')
        ax.set_ylabel('frequencies (Hz)')
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Amplitude (dB)')
        cbar.minorticks_on()
        return spec, freqs, t, im


def specgram3d(y, srate=44100, ax=None, title=None):
     if not ax:
        ax = plt.axes(projection='3d')
        ax.set_title(title, loc='center', wrap=True)
        spec, freqs, t = mlab.specgram(y, Fs=srate)
        X, Y, Z = t[None, :], freqs[:, None],  20.0 * np.log10(spec)
        ax.plot_surface(X, Y, Z, cmap='viridis')
        ax.set_ylabel('frequencies (Hz)')
        ax.set_ylabel('frequencies (Hz)')
        ax.set_zlabel('amplitude (dB)')
        ax.set_zlim(-140, 0)
        return X, Y, Z
