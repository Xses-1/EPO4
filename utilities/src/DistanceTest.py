import sys
import os
import numpy as np
import time

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'inc'))

from Audio import Audio
from wavaudioread import wavaudioread 

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fft import fft, ifft
from scipy.signal import convolve, unit_impulse, find_peaks
from scipy import linalg
import pickle

def ch3(x,y,Lhat,epsi):
    Nx = len(x)       # Length of x
    Ny = len(y)      # Length of y
    Nh = Lhat      
    
     # Length of h
    # Force x to be the same length as y
    x = np.concatenate((x, np.zeros(Ny-Nx)))
    
    # Deconvolution in frequency domain
    Y = fft(y)
    X = fft(x)
    H = Y/X
    # Threshold to avoid blow ups of noise during inversion
    H[np.absolute(X) < epsi*max(np.absolute(X))] = 0
    h = np.real(ifft(H))  # ensure the result is real
    #h = h[:Lhat] # optional: truncate to length Lhat (L is not reliable?)
    return h

def calculatedistanceof2samples(reference, sample1, sample2, Fs_RX):

  Lhat = len(sample1)
  epsi = 0.02
  h1 = ch3(reference,sample1,Lhat,epsi)
  h2 = ch3(reference,sample2,Lhat,epsi)

  argmax1 = np.argmax(h1)
  argmax2 = np.argmax(h2)

  if h1[argmax1] < 10**-9: # -8 is delete nothing
    return 0

  if h2[argmax2] < 10**-9: # -8 is delete nothing
    return 0
  
  timeDif = (argmax1 * 1/Fs_RX) - (argmax2 * 1/Fs_RX)

  return timeDif

def split_data(data):
    mic1 = data[0::5]
    mic4 = data[1::5]
    mic2 = data[2::5]
    mic3 = data[3::5]
    mic5 = data[4::5]
    return [mic1,mic2,mic3,mic4,mic5]

if __name__ == '__main__':
    objects = []
    with (open("reference.pkl", "rb")) as openfile:
        while True:
            try:
                objects.append(pickle.load(openfile))
            except EOFError:
                break

    ref = objects[0]

    objects = []
    with (open("runTestwithVideo.pkl", "rb")) as openfile:
        while True:
            try:
                objects.append(pickle.load(openfile))
            except EOFError:
                break

    


    stored = objects[0][1:]

    time.sleep(0.5)

    for i in stored:
        samples = split_data(i)

        firstPeak = np.max(samples[0])

        tau12 = calculatedistanceof2samples(ref, samples[0][: firstPeak + 40000], samples[1][: firstPeak + 40000], 44100)
        tau23 = calculatedistanceof2samples(ref, samples[1][: firstPeak + 40000], samples[2][: firstPeak + 40000], 44100)
        tau34 = calculatedistanceof2samples(ref, samples[2][: firstPeak + 40000], samples[3][: firstPeak + 40000], 44100)
        tau14 = calculatedistanceof2samples(ref, samples[0][: firstPeak + 40000], samples[3][: firstPeak + 40000], 44100)
        tau13 = calculatedistanceof2samples(ref, samples[0][: firstPeak + 40000], samples[2][: firstPeak + 40000], 44100)
        tau24 = calculatedistanceof2samples(ref, samples[1][: firstPeak + 40000], samples[3][: firstPeak + 40000], 44100)

        print(tau12, tau13, tau24, tau23)

        x1 = np.array([0, 0])
        x2 = np.array([0, 4.80])
        x3 = np.array([4.80, 4.80])
        x4 = np.array([4.80, 0])

        #Solving matrix A*B=C
        A = np.array([[2*(x2[0]-x1[0]), 2*(x2[1]-x1[1]),-2*tau12, 0, 0],[2*(x3[0]-x1[0]), 2*(x3[1]-x1[1]),0, -2*tau13, 0], 
                      [2*(x4[0]-x1[0]), 2*(x4[1]-x1[1]),0, 0, -2*tau14],[2*(x3[0]-x2[0]), 2*(x3[1]-x2[1]),0, -2*tau23, 0], 
                      [2*(x4[0]-x2[0]), 2*(x4[1]-x2[1]),0, 0, -2*tau24],[2*(x4[0]-x3[0]), 2*(x4[1]-x3[1]),0, 0, -2*tau34]])

        print('A',A)
        C = np.array([tau12**2-(np.linalg.norm(x1))**2+(np.linalg.norm(x2))**2, tau13**2-(np.linalg.norm(x1))**2+(np.linalg.norm(x3))**2,
                    tau14**2-(np.linalg.norm(x1))**2+(np.linalg.norm(x4))**2, tau23**2-(np.linalg.norm(x2))**2+(np.linalg.norm(x3))**2,
                    tau24**2-(np.linalg.norm(x2))**2+(np.linalg.norm(x4))**2, tau34**2-(np.linalg.norm(x3))**2+(np.linalg.norm(x4))**2])
        
        print('C', C)

        B = np.dot(np.linalg.pinv(A), C)

        print(B)
