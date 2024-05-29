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
        inc_value = 1000
        v = 343.21
        Lhat = len(y) - len(x) + 1

        plt.plot(y)

        x = x[len(x)-25000:]
        y = y[len(y)-25000:]

        #plt.plot(y)

        h0 = self.ch3(x, y[:, 0], Lhat, epsi)
        h1 = self.ch3(x, y[:, 1], Lhat, epsi)
        h2 = self.ch3(x, y[:, 2], Lhat, epsi)
        h3 = self.ch3(x, y[:, 3], Lhat, epsi)

        tau12 = ((abs(h0).argmax() - abs(h1).argmax())*v/Fs)
        tau23 = ((abs(h1).argmax() - abs(h2).argmax())*v/Fs)
        tau34 = ((abs(h2).argmax() - abs(h3).argmax())*v/Fs)
        tau14 = ((abs(h0).argmax() - abs(h3).argmax())*v/Fs)
        tau13 = ((abs(h0).argmax() - abs(h2).argmax())*v/Fs)
        tau24 = ((abs(h1).argmax() - abs(h3).argmax())*v/Fs)

        x1 = np.array([0, 0])
        x2 = np.array([0, 4.80])
        x3 = np.array([4.80, 4.80])
        x4 = np.array([4.80, 0])

        

        A = np.array([[ 2*(x2[0]-x1[0]).T,
                        2*(x2[1]-x1[1]).T,
                        -2*tau12, 0, 0],

                      [ 2*(x3[0]-x1[0]).T,
                        2*(x3[1]-x1[1]).T,
                        0, -2*tau13, 0],

                      [ 2*(x4[0]-x1[0]).T,
                        2*(x4[1]-x1[1]).T,
                        0, 0, -2*tau14],

                      [ 2*(x3[0]-x2[0]).T,
                        2*(x3[1]-x2[1]).T,
                        0, -2*tau23, 0],

                      [ 2*(x4[0]-x2[0]).T,
                        2*(x4[1]-x2[1]).T,
                        0, 0, -2*tau24],

                      [ 2*(x4[0]-x3[0]).T,
                        2*(x4[1]-x3[1]).T,
                        0, 0, -2*tau34]])

        C = np.array([  tau12**2-(np.linalg.norm(x1))**2+(np.linalg.norm(x2))**2,
                        tau13**2-(np.linalg.norm(x1))**2+(np.linalg.norm(x3))**2,
                        tau14**2-(np.linalg.norm(x1))**2+(np.linalg.norm(x4))**2,
                        tau23**2-(np.linalg.norm(x2))**2+(np.linalg.norm(x3))**2,
                        tau24**2-(np.linalg.norm(x2))**2+(np.linalg.norm(x4))**2,
                        tau34**2-(np.linalg.norm(x3))**2+(np.linalg.norm(x4))**2])

        B = np.dot(np.linalg.pinv(A), C)


        return B

    def closest_mic(self, X, Y):
        if (X < 240) and (Y < 240):
            the_closest_mic = 1

        elif (X < 240) and (Y > 240):
            the_closest_mic = 2

        elif (X > 240) and (Y > 240):
            the_closest_mic = 3

        else:
            the_closest_mic = 4

        return the_closest_mic

    def error_correction(self, X, Y, cl_mic):
        l = X**2 + Y**2
        Xn = X
        Yn = Y
        Z = 25

        if (cl_mic == 1):
            while (Xn**2 + Yn**2 + Z**2) < l:
                Xn = Xn + 1
                Yn = Yn + 1

        elif (cl_mic == 2):
            while (Xn**2 + Yn**2 + Z**2) < l:
                Xn = Xn - 1
                Yn = Yn + 1

        elif rcl_mic == 3):
            while (Xn**2 + Yn**2 + Z**2) < l:
                Xn = Xn - 1
                Yn = Yn - 1

        else:
            while (Xn**2 + Yn**2 + Z**2) < l:
                Xn = Xn - 1
                Yn = Yn - 1

        return Xn, Yn

        
    
Fs = 44100

a = wavaudioread("reference.wav", Fs)
a = a[:,0]
b = wavaudioread("record_x143_y296.wav", Fs)

T = TDOA()
c = T.localization(a,b,Fs)

# Testing before the error compensation
error = np.sqrt((1.43-c[0])**2+(2.96-c[1])**2)
print(error)
print(c)

# c structure:
# X, Y, distance to mic 2, distance to mic 3, distance to mic 4
X = c[0] * 100
Y = c[1] * 100

# First find the closes mic, so in which quadrant are we in
cl_mic = T.closest_mic(X, Y)
print (cl_mic)

# Now try to correct for the error
X, Y = error_correction(X, Y, cl_mic)
print(X, Y)
