import sys
import os

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'inc'))

from Audio import Audio

if __name__ == '__main__':
    mics = Audio()

    N = 44100 * 2

    data = mics.sample(N)#
    samples = mics.split_data(data)

    mics.writeto1Wav(samples[0], samples[1], samples[2], samples[3], samples[4], filename = 'beaconTestx250y250.wav')
