import sys
import os
import numpy as np
import time

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'inc'))

from Audio import Audio
from TDOA import TDOA
from wavaudioread import wavaudioread 

if __name__ == '__main__':
    mics = Audio()
    TD = TDOA()
    N = int(44100 * 1)

    ref = wavaudioread("BeaconReference.wav", mics.Fs)

    time.sleep(0.5)

    while True:
        samples = mics.split_data(mics.sample(N))
        
        print(TD.localization(ref, np.array(samples).T, mics.Fs))
