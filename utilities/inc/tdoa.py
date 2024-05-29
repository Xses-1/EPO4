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
        h4 = self.ch3(x, y[:, 4], Lhat, epsi)

        fig, ax = plt.subplots(3,2,figsize=(15,8))

        ax[0,0].plot(abs(h0))
        ax[0,1].plot(abs(h1))
        ax[1,0].plot(abs(h2))
        ax[1,1].plot(abs(h3))
        ax[2,0].plot(abs(h4))
        fig.tight_layout()
        plt.show()

        tau12 = ((abs(h0).argmax() - abs(h1).argmax())*v/Fs)
        tau23 = ((abs(h1).argmax() - abs(h2).argmax())*v/Fs)
        tau34 = ((abs(h2).argmax() - abs(h3).argmax())*v/Fs)
        tau14 = ((abs(h0).argmax() - abs(h3).argmax())*v/Fs)
        tau13 = ((abs(h0).argmax() - abs(h2).argmax())*v/Fs)
        tau24 = ((abs(h1).argmax() - abs(h3).argmax())*v/Fs)
        tau15 = ((abs(h0).argmax() - abs(h4).argmax())*v/Fs)
        tau25 = ((abs(h1).argmax() - abs(h4).argmax())*v/Fs)
        tau35 = ((abs(h2).argmax() - abs(h4).argmax())*v/Fs)
        tau45 = ((abs(h3).argmax() - abs(h4).argmax())*v/Fs)

        print(tau12,tau23,tau34,tau14,tau13,tau24,tau15,tau25,tau35,tau45)

        x1 = np.array([0, 0, 0.252])
        x2 = np.array([0, 4.80, 0.252])
        x3 = np.array([4.80, 4.80, 0.252])
        x4 = np.array([4.80, 0, 0.252])
        x5 = np.array([0, 2.40, 0.552])

        

        A = np.array([[2*np.transpose(x2[0]-x1[0]), 2*np.transpose(x2[1]-x1[1]), 2*np.transpose(x2[2]-x1[2]),-2*tau12, 0, 0, 0],
	                 [2*np.transpose(x3[0]-x1[0]), 2*np.transpose(x3[1]-x1[1]), 2*np.transpose(x3[2]-x1[2]),0, -2*tau13, 0, 0], 
                     [2*np.transpose(x4[0]-x1[0]), 2*np.transpose(x4[1]-x1[1]), 2*np.transpose(x4[2]-x1[2]),0, 0, -2*tau14, 0],
                     [2*np.transpose(x5[0]-x1[0]), 2*np.transpose(x5[1]-x1[1]), 2*np.transpose(x5[2]-x1[2]),0, 0, 0, -2*tau15], 
                     [2*np.transpose(x3[0]-x2[0]), 2*np.transpose(x3[1]-x2[1]), 2*np.transpose(x3[2]-x2[2]),0, -2*tau23, 0, 0], 
                     [2*np.transpose(x4[0]-x2[0]), 2*np.transpose(x4[1]-x2[1]), 2*np.transpose(x4[2]-x2[2]),0, 0, -2*tau24, 0],
                     [2*np.transpose(x5[0]-x2[0]), 2*np.transpose(x5[1]-x2[1]), 2*np.transpose(x5[2]-x2[2]),0, 0, 0, -2*tau25], 
                     [2*np.transpose(x4[0]-x3[0]), 2*np.transpose(x4[1]-x3[1]), 2*np.transpose(x4[2]-x3[2]),0, 0, -2*tau34, 0],
                     [2*np.transpose(x5[0]-x3[0]), 2*np.transpose(x5[1]-x3[1]), 2*np.transpose(x5[2]-x3[2]),0, 0, 0, -2*tau35],
                     [2*np.transpose(x5[0]-x4[0]), 2*np.transpose(x5[1]-x4[1]), 2*np.transpose(x5[2]-x4[2]),0, 0, 0, -2*tau45] ])

        C = np.array([tau12**2-(np.linalg.norm(x1))**2+(np.linalg.norm(x2))**2, 
                      tau13**2-(np.linalg.norm(x1))**2+(np.linalg.norm(x3))**2,
                      tau14**2-(np.linalg.norm(x1))**2+(np.linalg.norm(x4))**2,
                      tau15**2-(np.linalg.norm(x1))**2+(np.linalg.norm(x5))**2,
                      tau23**2-(np.linalg.norm(x2))**2+(np.linalg.norm(x3))**2,
                      tau24**2-(np.linalg.norm(x2))**2+(np.linalg.norm(x4))**2,
                      tau25**2-(np.linalg.norm(x2))**2+(np.linalg.norm(x5))**2, 
                      tau34**2-(np.linalg.norm(x3))**2+(np.linalg.norm(x4))**2,
                      tau35**2-(np.linalg.norm(x3))**2+(np.linalg.norm(x5))**2,
                      tau45**2-(np.linalg.norm(x4))**2+(np.linalg.norm(x5))**2])

        B = np.dot(np.linalg.pinv(A), C)
        #B = np.linalg.lstsq(A, C, rcond=None)[0]
        return B
    
Fs = 44100

a = wavaudioread("reference.wav", Fs)
a = a[:,0]
b = wavaudioread("record_x143_y296.wav", Fs)

T = TDOA()
c = T.localization(a,b,Fs)

error = np.sqrt((1.43-c[0])**2+(2.96-c[1])**2)
print(error)

print(c)
