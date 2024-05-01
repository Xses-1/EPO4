import sys
import os

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'inc'))

from Audio import Audio

if __name__ == '__main__':
    mics = Audio()

    data = mics.sample(80000) * 10
    samples = mics.split_data(data)

    mics.play_sound(samples[0])

    mics.writeAlltoWave(samples[0], samples[1], samples[2], samples[3], samples[4], fileappendix = 'beacon')