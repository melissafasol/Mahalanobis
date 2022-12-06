import os 
import numpy as np
from scipy import signal 
from scipy.fft import fftshift
from matplotlib import mlab
import matplotlib.pyplot as plt


def specgram2d(data, srate, ax=None, title=None, ymin, ymax):
    if not ax:
        ax = plt.axes()
        ax.set_title(title, loc='center', wrap=True)
        spec, freqs, t, im = ax.specgram(data, Fs=srate, scale='dB', vmax=0)
        ax.set_xlabel('time (s)')
        ax.set_ylabel('frequencies (Hz)')
        ax.set_ylim(ymin = ymin, ymax  = ymax)
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Amplitude (mV)')
        cbar.minorticks_on()
        return spec, freqs, t, im


def specgram3d(data, srate, ax=None, title=None, ymin, ymax):
     if not ax:
        ax = plt.axes(projection='3d')
        ax.set_title(title, loc='center', wrap=True)
        spec, freqs, t = mlab.specgram(data, Fs=srate)
        X, Y, Z = t[None, :], freqs[:, None],  20.0 * np.log10(spec)
        ax.plot_surface(X, Y, Z, cmap='viridis')
        ax.set_ylim(ymin = ymin, ymax = ymax)
        ax.set_ylabel('frequencies (Hz)')
        ax.set_ylabel('frequencies (Hz)')
        ax.set_zlabel('amplitude (mV)')
        #ax.set_zlim(-140, 0)
        return X, Y, Z
