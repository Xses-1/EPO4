import sys
import os

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'inc'))

from Audio import Audio

if __name__ == '__main__':
    mics = Audio()

    samples = mics.split_data(mics.sample(5000))

    mics.play_sound(samples[0])