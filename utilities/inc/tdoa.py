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
        epsi = 0.01     #threshold value used in ch3
        v = 343.21      #speed of sound
        Lhat1 = len(y) - len(x1) + 1    #equal length of x and y 
        Lhat2 = len(y) - len(x2) + 1
        Lhat3 = len(y) - len(x3) + 1
        Lhat4 = len(y) - len(x4) + 1
        Lhat5 = len(y) - len(x5) + 1
    
        x1 = x1[len(x1)-25000:]         #crop x to the last pulse(s)
        x2 = x2[len(x2)-25000:]
        x3 = x3[len(x3)-25000:]
        x4 = x4[len(x4)-25000:]
        x5 = x5[len(x5)-25000:]

        y = y[len(y)-25000:]            #crop y to the last pulse(s)

        h0 = self.ch3(x1, y[:, 0], Lhat1, epsi)     #create the channel estimates for all microphones
        h1 = self.ch3(x1, y[:, 1], Lhat2, epsi)
        h2 = self.ch3(x1, y[:, 2], Lhat3, epsi)
        h3 = self.ch3(x1, y[:, 3], Lhat4, epsi)
        h4 = self.ch3(x1, y[:, 4], Lhat5, epsi)

        tau12 = ((abs(h0).argmax() - abs(h1).argmax())*v/Fs) #calculate the difference between peaks
        tau14 = ((abs(h0).argmax() - abs(h3).argmax())*v/Fs) #in the channel estimates
        tau13 = ((abs(h0).argmax() - abs(h2).argmax())*v/Fs)
        tau15 = ((abs(h0).argmax() - abs(h4).argmax())*v/Fs)

        p1 = np.array([0, 0])       #define microphone positions
        p2 = np.array([0, 4.60])
        p3 = np.array([4.60, 4.60])
        p4 = np.array([4.60, 0])
        p5 = np.array([0, 2.30])
        
        A = np.array([[p1[0]-p2[0],p1[1]-p2[1],tau12],      
                      [p1[0]-p3[0],p1[1]-p3[1],tau13],
                      [p1[0]-p4[0],p1[1]-p4[1],tau14],
                      [p1[0]-p5[0],p1[1]-p5[1],tau15]])
        
        C = np.array([[0.5*(p1[0]**2-p2[0]**2+p1[1]**2-p2[1]**2+tau12**2)],
                      [0.5*(p1[0]**2-p3[0]**2+p1[1]**2-p3[1]**2+tau13**2)],
                      [0.5*(p1[0]**2-p4[0]**2+p1[1]**2-p4[1]**2+tau14**2)],
                      [0.5*(p1[0]**2-p5[0]**2+p1[1]**2-p5[1]**2+tau15**2)]])

        B = np.linalg.lstsq(A, C, rcond=None)[0][:2].flatten()  #matrix calculation to get coordinates

        #print(B)
        return B

    def closest_mic(self, X, Y):
        if (X < 230) and (Y < 230):
            the_closest_mic = 1

        elif (X < 230) and (Y > 230):
            the_closest_mic = 2

        elif (X > 230) and (Y > 230):
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
        b = np.stack((mic1, mic2, mic3, mic4, mic5), axis =-1) #takes input arrays and stacks them in a 3d array
                                                               #with each column containing a different microphone
        return b
