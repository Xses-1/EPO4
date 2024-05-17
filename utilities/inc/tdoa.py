import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fft import fft, ifft
from scipy.signal import convolve, unit_impulse, find_peaks
from scipy import linalg
#from refsignal import refsignal



class TDOA:
    def ch3(self,x,y,Lhat,epsi):
        Nx = len(x)       # Length of x
        Ny = len(y)      # Length of y
        Nh = Lhat       # Length of h

        #print(Nx, Ny)

        # Force x to be the same length as y
        x = np.concatenate((x, np.zeros(Ny-Nx)))
        
        #print(y)
        # Deconvolution in frequency domain
        Y = fft(y)
        X = fft(x)
        H = Y/X

        # Threshold to avoid blow ups of noise during inversion
        H[np.absolute(X) < epsi*max(np.absolute(X))] = 0

        h = np.real(ifft(H))  # ensure the result is real
        #h = h[:Lhat] # optional: truncate to length Lhat (L is not reliable?)
        return h

    def localization(self, x, y, Fs):
        epsi = 0.01
        inc_value = 1000
        v = 343
        Lhat = len(y) - len(x) + 1
        h0 = self.ch3(x, y[:, 0], Lhat, epsi)
        h1 = self.ch3(x, y[:, 1], Lhat, epsi)
        h2 = self.ch3(x, y[:, 2], Lhat, epsi)
        h3 = self.ch3(x, y[:, 3], Lhat, epsi)
        # plt.plot(y)
        # plt.title("Recording 2")
        # plt.xlabel("Samples")
        # plt.ylabel("Magnitude")

        #print('test')
        #print(y, x, Lhat)
        #print('test')
        # find peaks
        incrementx = find_peaks(x, height=x[x.argmax()]*0.4)
        increment0 = find_peaks(h0, height=h0[h0.argmax()]*0.4)
        increment1 = find_peaks(h1, height=h1[h1.argmax()]*0.4)
        increment2 = find_peaks(h2, height=h2[h2.argmax()]*0.4)
        increment3 = find_peaks(h3, height=h3[h3.argmax()]*0.4)

        

        #define increments
        incx0 = int(incrementx[0][0] - inc_value)
        incx1 = int(incrementx[0][0] + inc_value)
        #inc0 = int(increment0[0][0] - inc_value)
        inc01 = int(increment0[0][0] + inc_value)
        #inc1 = int(increment1[0][0] - inc_value)
        inc11 = int(increment1[0][0] + inc_value)
        #inc2 = int(increment2[0][0] -inc_value)
        inc21 = int(increment2[0][0] +inc_value)
        #inc3 = int(increment3[0][0] -inc_value)
        inc31 = int(increment3[0][0] +inc_value)

        #plt.plot(x[incx0:incx1])
        #plt.title("Reference signal peak")
        #plt.xlabel("Samples")
        #plt.ylabel("Magnitude")

        # fig, ax = plt.subplots(2, 2, figsize=(13, 8))

        # #ax[0,0].set_title("Reference signal")
        # #ax[0,0].plot(x[incx0:incx1])
        # ax[0,0].set_title("Selected peak recording 2, channel 1")
        # ax[0,0].plot(y[incx0:inc01,0])
        # ax[0,0].set_xlabel("Samples")
        # ax[0,0].set_ylabel("Magnitude")
        # ax[0,1].set_title("Selected peak recording 2, channel 2")
        # ax[0,1].plot(y[incx0:inc11,0])
        # ax[0,1].set_xlabel("Samples")
        # ax[0,1].set_ylabel("Magnitude")
        # ax[1,0].set_title("Selected peak recording 2, channel 3")
        # ax[1,0].plot(y[incx0:inc21,0])
        # ax[1,0].set_xlabel("Samples")
        # ax[1,0].set_ylabel("Magnitude")
        # ax[1,1].set_title("Selected peak recording 2, channel 4")
        # ax[1,1].plot(y[incx0:inc31,0])
        # ax[1,1].set_xlabel("Samples")
        # ax[1,1].set_ylabel("Magnitude")
        # fig.tight_layout()
        #print(incx0, incx1, inc01, inc11)
        #channel modulation


        fig, ax = plt.subplots(2, 2, figsize=(15, 8))

        ax[0,0].set_title("Recording 2, channel 1")
        ax[0,0].plot(abs(h0))
        ax[0,0].set_xlabel("Samples")
        ax[0,0].set_ylabel("Magnitude")
        ax[0,1].set_title("Recording 2, channel 2")
        ax[0,1].plot(abs(h1))
        ax[0,1].set_xlabel("Samples")
        ax[0,1].set_ylabel("Magnitude")
        ax[1,0].set_title("Recording 2, channel 3")
        ax[1,0].plot(abs(h2))
        ax[1,0].set_xlabel("Samples")
        ax[1,0].set_ylabel("Magnitude")
        ax[1,1].set_title("Recording 2, channel 4")
        ax[1,1].plot(abs(h3))
        ax[1,1].set_xlabel("Samples")
        ax[1,1].set_ylabel("Magnitude")

        #defining tau
        tau12 = (abs(h0[incx0:inc01]).argmax() - abs(h1[incx0:inc11]).argmax())*v/Fs
        tau23 = (abs(h1[incx0:inc11]).argmax() - abs(h2[incx0:inc21]).argmax())*v/Fs
        tau34 = (abs(h2[incx0:inc21]).argmax() - abs(h3[incx0:inc31]).argmax())*v/Fs
        tau14 = (abs(h0[incx0:inc01]).argmax() - abs(h3[incx0:inc31]).argmax())*v/Fs
        tau13 = (abs(h0[incx0:inc01]).argmax() - abs(h2[incx0:inc21]).argmax())*v/Fs
        tau24 = (abs(h1[incx0:inc11]).argmax() - abs(h3[incx0:inc31]).argmax())*v/Fs

        #print(tau12,tau23,tau34,tau14,tau13,tau24)

        #defining mic locations
        x1 = np.array([0, 0])
        x2 = np.array([0, 4.80])
        x3 = np.array([4.80, 4.80])
        x4 = np.array([4.80, 0])

        #Solving matrix A*B=C
        A = np.array([[2*(x2[0]-x1[0]), 2*(x2[1]-x1[1]),-2*tau12, 0, 0],[2*(x3[0]-x1[0]), 2*(x3[1]-x1[1]),0, -2*tau13, 0], 
                      [2*(x4[0]-x1[0]), 2*(x4[1]-x1[1]),0, 0, -2*tau14],[2*(x3[0]-x2[0]), 2*(x3[1]-x2[1]),0, -2*tau23, 0], 
                      [2*(x4[0]-x2[0]), 2*(x4[1]-x2[1]),0, 0, -2*tau24],[2*(x4[0]-x3[0]), 2*(x4[1]-x3[1]),0, 0, -2*tau34]])

        C = np.array([tau12**2-(np.linalg.norm(x1))**2+(np.linalg.norm(x2))**2, tau13**2-(np.linalg.norm(x1))**2+(np.linalg.norm(x3))**2,
                    tau14**2-(np.linalg.norm(x1))**2+(np.linalg.norm(x4))**2, tau23**2-(np.linalg.norm(x2))**2+(np.linalg.norm(x3))**2,
                    tau24**2-(np.linalg.norm(x2))**2+(np.linalg.norm(x4))**2, tau34**2-(np.linalg.norm(x3))**2+(np.linalg.norm(x4))**2])

        B = np.dot(np.linalg.pinv(A), C)
        fig.tight_layout()
        plt.show()
        return B

import samplerate
from scipy.io import wavfile


def wavaudioread(filename, fs):
    fs_wav, y_wav = wavfile.read(filename)
    y = samplerate.resample(y_wav, fs / fs_wav, "sinc_best")

    return y

Fs = 44100
a = wavaudioread("reference.wav", Fs)

a = a[:,0]


#b = wavaudioread("record_x232_y275.wav", Fs)
b = wavaudioread("record_x_y_hidden_3.wav", Fs)


T = TDOA()
c = T.localization(a,b,Fs)

#error = np.sqrt((2.32-c[0])**2+(2.75-c[1])**2)

#print(error)

print(c)