import sys
import os
import time
import pickle
import numpy as np
import keyboard

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'inc'))

from Audio import Audio

mics = Audio(callback = False)

allData = []
while True: 
    N = int(44100 * 0.5)
    data = mics.sample(N)#this is still blocking :(

    allData.append(data)
    if keyboard.is_pressed('escape'):
        break

print(len(allData), len(allData[2]))

with open('runTestwithVideo.pkl', 'wb') as outp:
    pickle.dump(allData, outp, pickle.HIGHEST_PROTOCOL)

mics.close()
    

