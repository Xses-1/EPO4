import matplotlib.pyplot as plt
import pickle
import numpy as np
import sys
import os
from scipy.signal import convolve, unit_impulse, find_peaks


sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'inc'))

from Audio import Audio

objects = []
with (open("reference.pkl", "rb")) as openfile:
    while True:
        try:
            objects.append(pickle.load(openfile))
        except EOFError:
            break

print(np.array(objects[0]))

print(max(objects[0]))

plt.plot(objects[0][:10000])

plt.show()

ref = objects[0]

with open('reference.pkl', 'wb') as outp:
    pickle.dump(ref, outp, pickle.HIGHEST_PROTOCOL)