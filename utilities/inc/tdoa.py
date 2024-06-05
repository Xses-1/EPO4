
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

    def localization(self, x1,x2,x3,x4,x5, y, Fs):
        epsi = 0.01
        v = 343.21
        Lhat1 = len(y) - len(x1) + 1
        Lhat2 = len(y) - len(x2) + 1
        Lhat3 = len(y) - len(x3) + 1
        Lhat4 = len(y) - len(x4) + 1
        Lhat5 = len(y) - len(x5) + 1
    
        x1 = x1[len(x1)-25000:]
        x2 = x2[len(x2)-25000:]
        x3 = x3[len(x3)-25000:]
        x4 = x4[len(x4)-25000:]
        x5 = x5[len(x5)-25000:]


        y = y[len(y)-25000:]

        plt.plot(y[:,0])

        h0 = self.ch3(x1, y[:, 0], Lhat1, epsi)
        h1 = self.ch3(x2, y[:, 1], Lhat2, epsi)
        h2 = self.ch3(x3, y[:, 2], Lhat3, epsi)
        h3 = self.ch3(x4, y[:, 3], Lhat4, epsi)
        h4 = self.ch3(x5, y[:, 4], Lhat5, epsi)

        fig, ax = plt.subplots(2, 2, figsize=(15, 8))

        ax[0,0].set_title("Recording 1, channel 1")
        ax[0,0].plot(abs(h0))
        ax[0,0].set_xlabel("Samples")
        ax[0,0].set_ylabel("Magnitude")
        ax[0,1].set_title("Recording 1, channel 2")
        ax[0,1].plot(abs(h1))
        ax[0,1].set_xlabel("Samples")
        ax[0,1].set_ylabel("Magnitude")
        ax[1,0].set_title("Recording 1, channel 3")
        ax[1,0].plot(abs(h2))
        ax[1,0].set_xlabel("Samples")
        ax[1,0].set_ylabel("Magnitude")
        ax[1,1].set_title("Recording 1, channel 4")
        ax[1,1].plot(abs(h3))
        ax[1,1].set_xlabel("Samples")
        ax[1,1].set_ylabel("Magnitude")
        fig.tight_layout()
        plt.show()

        print(abs(h0).argmax())
        print(abs(h1).argmax())
        print(abs(h2).argmax())
        print(abs(h3).argmax())
        print(abs(h4).argmax())

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

        #print(B)
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

        elif (cl_mic == 3):
            while (Xn**2 + Yn**2 + Z**2) < l:
                Xn = Xn - 1
                Yn = Yn - 1

        else:
            while (Xn**2 + Yn**2 + Z**2) < l:
                Xn = Xn - 1
                Yn = Yn - 1

        return Xn, Yn

    def tdoa_input(self,mic1,mic2,mic3,mic4,mic5): 
        b = []
        b = np.stack((mic1, mic2, mic3, mic4, mic5), axis =-1)

        return b
