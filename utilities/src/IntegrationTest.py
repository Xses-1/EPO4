import sys
import os
import numpy as np
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'inc'))
from wavaudioread import wavaudioread
from Audio import Audio 
from var_ref_tdoa import TDOA

if __name__ == '__main__':
    mics = Audio()
    N = 44100 * 1
    data = mics.sample(N)#
    samples = mics.split_data(data)

    T = TDOA()
    y = T.tdoa_input(samples[0], samples[1], samples[2], samples[3], samples[4])

    Fs = 44100
    root_folder = Path("IntegrationTest.py").resolve().parent
    
    x1 = wavaudioread(root_folder / "utilities/data/Reference1.wav", Fs)    #Using reference recordings from all microphones
    x2 = wavaudioread(root_folder / "utilities/data/Reference2.wav", Fs)    #Every channel estimate/microphone uses it's own 
    x3 = wavaudioread(root_folder / "utilities/data/Reference3.wav", Fs)    #reference signal
    x4 = wavaudioread(root_folder / "utilities/data/Reference4.wav", Fs)
    x5 = wavaudioread(root_folder / "utilities/data/Reference5.wav", Fs)
    #x = x[:,0]

    c = T.localization(x1,x2,x3,x4,x5, y, Fs)
    print(c)

    error = np.sqrt((3.25-c[0])**2+(1.60-c[1])**2)

    print(error)
