import sys
import os
import numpy as np
import time


sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'inc'))
from wavaudioread import wavaudioread
from Audio import Audio 
from tdoa import TDOA



if __name__ == '__main__':
    mics = Audio()
    N = 44100 * 1
    data = mics.sample(N)#
    a1 = mics.split_data(data)
    samples = mics.split_data(data)
    T = TDOA()
    print(a1)
    y = T.tdoa_input(a1[0], a1[1], a1[2], a1[3], a1[4])
    Fs = 44100
    x = wavaudioread("BeaconReference.wav", Fs)
    x = x[:,0]

    c = T.localization(x, y, Fs)
