import sys
import os
import numpy as np
import time

import pyaudio
from scipy.io.wavfile import write
import sys
import pickle
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fft import fft, ifft
from scipy.signal import convolve, unit_impulse
from scipy import linalg
import samplerate

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'inc'))

from Audio import Audio 
from tdoa import TDOA

if __name__ == '__main__':
    mics = Audio()
    N = 44100 * 1
    data = mics.sample(N)#
    a1 = mics.split_data(data)
    T = TDOA()
    y = T.tdoa_input(mic1, mic2, mic3, mic4, mic5)
    Fs = 44100
    x = waveaudioread("reference.wav", Fs)
    x = x[:,0]

    c = T.localization(x, y, Fs)
