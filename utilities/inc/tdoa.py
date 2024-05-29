#!/bin/python3.10
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fft import fft, ifft
from scipy.signal import convolve, unit_impulse
from scipy import linalg

import samplerate
from scipy.io import wavfile


def wavaudioread(filename, fs):
    fs_wav, y_wav = wavfile.read(filename)
    y = samplerate.resample(y_wav, fs / fs_wav, "sinc_best")

    return y

class TDOA:
    def ch3(self,x,y,Lhat,epsi):
        Nx = len(x)       
        Ny = len(y)      
        Nh = Lhat 

        x = np.concatenate((x, np.zeros(Ny-Nx)))

        Y = fft(y)
        X = fft(x)
        H = Y/X

        H[np.absolute(X) < epsi*max(np.absolute(X))] = 0
        h = np.real(ifft(H)) 

        return h

    def localization(self, x, y, Fs):
        epsi = 0.01
        v = 343.21
        Lhat = len(y) - len(x) + 1
    
        x = x[len(x)-25000:]
        y = y[len(y)-25000:]

        h0 = self.ch3(x, y[:, 0], Lhat, epsi)
        h1 = self.ch3(x, y[:, 1], Lhat, epsi)
        h2 = self.ch3(x, y[:, 2], Lhat, epsi)
        h3 = self.ch3(x, y[:, 3], Lhat, epsi)
        h4 = self.ch3(x, y[:, 4], Lhat, epsi)

        tau12 = ((abs(h0).argmax() - abs(h1).argmax())*v/Fs)
        tau14 = ((abs(h0).argmax() - abs(h3).argmax())*v/Fs)
        tau13 = ((abs(h0).argmax() - abs(h2).argmax())*v/Fs)
        tau15 = ((abs(h0).argmax() - abs(h4).argmax())*v/Fs)

        x1 = np.array([0, 0])
        x2 = np.array([0, 4.80])
        x3 = np.array([4.80, 4.80])
        x4 = np.array([4.80, 0])
        x5 = np.array([0, 2.40])
        
        A = np.array([[x1[0]-x2[0],x1[1]-x2[1],tau12],
                      [x1[0]-x3[0],x1[1]-x3[1],tau13],
                      [x1[0]-x4[0],x1[1]-x4[1],tau14],
                      [x1[0]-x5[0],x1[1]-x5[1],tau15]])
        
        C = np.array([[0.5*(x1[0]**2-x2[0]**2+x1[1]**2-x2[1]**2+tau12**2)],
                      [0.5*(x1[0]**2-x3[0]**2+x1[1]**2-x3[1]**2+tau13**2)],
                      [0.5*(x1[0]**2-x4[0]**2+x1[1]**2-x4[1]**2+tau14**2)],
                      [0.5*(x1[0]**2-x5[0]**2+x1[1]**2-x5[1]**2+tau15**2)]])

        B = np.linalg.lstsq(A, C, rcond=None)[0][:2].flatten()

        print(B)
        return B
    
Fs = 44100

a = wavaudioread("reference.wav", Fs)
a = a[:,0]
#b = wavaudioread("record_x232_y275.wav", Fs)
b = wavaudioread("record_x4_y_hidden_1.wav", Fs)

T = TDOA()
c = T.localization(a,b,Fs)

error = np.sqrt((1.43-c[0])**2+(2.96-c[1])**2)
print(error)
