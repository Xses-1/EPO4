import sys
import os
import pickle

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'inc'))

from Audio import Audio

if __name__ == '__main__':
    mics = Audio()
    N = 44100 * 1
    data = mics.sample(N)#
    samples = mics.split_data(data)

    with open('reference.pkl', 'wb') as outp:
        pickle.dump(samples[0], outp, pickle.HIGHEST_PROTOCOL)