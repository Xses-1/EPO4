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

        print(Nx, Ny)

        # Force x to be the same length as y
        x = np.concatenate((x, np.zeros(Ny-Nx)))
        
        print(y)
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
        epsi = 0.005
        inc_value = 1000
        v = 343
        Lhat = len(y) - len(x) + 1

        print('test')
        print(y, x, Lhat)
        print('test')
        # find peaks
        incrementx = find_peaks(x, height=x[x.argmax()]*0.4)
        increment0 = find_peaks(y[:,0], height=y[:,0][y[:,0].argmax()]*0.4)
        increment1 = find_peaks(y[:,1], height=y[:,1][y[:,1].argmax()]*0.4)
        increment2 = find_peaks(y[:,2], height=y[:,2][y[:,2].argmax()]*0.4)
        increment3 = find_peaks(y[:,3], height=y[:,3][y[:,3].argmax()]*0.4)

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

        print(incx0, incx1, inc01, inc11)
        #channel modulation
        h0 = self.ch3(x[incx0:incx1], y[incx0:inc01, 0], Lhat, epsi)
        h1 = self.ch3(x[incx0:incx1], y[incx0:inc11, 1], Lhat, epsi)
        h2 = self.ch3(x[incx0:incx1], y[incx0:inc21, 2], Lhat, epsi)
        h3 = self.ch3(x[incx0:incx1], y[incx0:inc31, 3], Lhat, epsi)

        #defining tau
        tau12 = (h0.argmax() - h1.argmax())*v/Fs
        tau23 = (h1.argmax() - h2.argmax())*v/Fs
        tau34 = (h2.argmax() - h3.argmax())*v/Fs
        tau14 = (h0.argmax() - h3.argmax())*v/Fs
        tau13 = (h0.argmax() - h2.argmax())*v/Fs
        tau24 = (h1.argmax() - h3.argmax())*v/Fs

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

        return B