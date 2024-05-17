import sys
import os
import time
import pickle
import numpy as np
import keyboard

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'inc'))

from Audio import Audio

mics = Audio(callback = True)

allData = []
while True:
    time.sleep(0.1)

    allData += mics.callback_data

    if keyboard.is_pressed('escape'):
        break

print(len(allData))

with open('runTest.pkl', 'wb') as outp:
    pickle.dump(allData, outp, pickle.HIGHEST_PROTOCOL)

mic1,mic2,mic3,mic4,mic5 = mics.split_data(allData)

mics.writeAlltoWave(mic1,mic2,mic3,mic4,mic5, fileappendix = 'RunaroundTest')

mics.close()
    

