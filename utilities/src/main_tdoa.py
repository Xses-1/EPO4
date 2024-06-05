import sys
import os
import numpy as np

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'inc'))
from wavaudioread import wavaudioread
from Audio import Audio 
from tdoa import TDOA

class main_tdoa:
    def location(self):
        if __name__ == '__main__':
            N = 44100 * 1
            Fs = 44100
            x = wavaudioread("reference.wav", Fs)
            x = x[:,0]

            mics = Audio(callback = True)
            data = mics.callback_data
            samples = mics.split_data(data)
            
            T = TDOA()
            y = T.tdoa_input(samples[0], samples[1], samples[2], samples[3], samples[4])
            c = T.localization(x, y, Fs)

            return c
