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
        def channel_estimate(x1,x2,x3,x4,x5,y,Fs):
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
            h1 = self.ch3(x2, y[:, 1], Lhat2, epsi)
            h2 = self.ch3(x3, y[:, 2], Lhat3, epsi)
            h3 = self.ch3(x4, y[:, 3], Lhat4, epsi)
            h4 = self.ch3(x5, y[:, 4], Lhat5, epsi)

            return h0, h1, h2, h3, h4
        
        def closest_mic(h0,h1,h2,h3):
            distances = np.array([[abs(h0).argmax()], [abs(h1).argmax()], [abs(h2).argmax()], [abs(h3).argmax()]]) #array of all peaks
            min_pos = np.argmin(distances) + 1  #takes the indice of peak with the lowest sample number, adds 1 to get the corresponding mic number
            #print(min_pos)
            return min_pos

        def matrix_calc(h0,h1,h2,h3,h4,cl_mic):
            v = 343.21      #speed of sound
            p1 = np.array([0, 0])       #define microphone positions ####PAY ATTENTION TO 480/460###
            p2 = np.array([0, 4.80])
            p3 = np.array([4.80, 4.80])
            p4 = np.array([4.80, 0])
            p5 = np.array([0, 2.40])
    
            if cl_mic == 1:
                tau12 = ((abs(h0).argmax() - abs(h1).argmax())*v/Fs) #calculate the difference between peaks
                tau14 = ((abs(h0).argmax() - abs(h3).argmax())*v/Fs) #in the channel estimates
                tau13 = ((abs(h0).argmax() - abs(h2).argmax())*v/Fs)
                tau15 = ((abs(h0).argmax() - abs(h4).argmax())*v/Fs)

                A = np.array([[p1[0]-p2[0],p1[1]-p2[1],tau12],      
                            [p1[0]-p3[0],p1[1]-p3[1],tau13],
                            [p1[0]-p4[0],p1[1]-p4[1],tau14],
                            [p1[0]-p5[0],p1[1]-p5[1],tau15]])
        
                C = np.array([[0.5*(p1[0]**2-p2[0]**2+p1[1]**2-p2[1]**2+tau12**2)],
                            [0.5*(p1[0]**2-p3[0]**2+p1[1]**2-p3[1]**2+tau13**2)],
                            [0.5*(p1[0]**2-p4[0]**2+p1[1]**2-p4[1]**2+tau14**2)],
                            [0.5*(p1[0]**2-p5[0]**2+p1[1]**2-p5[1]**2+tau15**2)]])

                B = np.linalg.lstsq(A, C, rcond=None)[0][:2].flatten()  #matrix calculation to get coordinates
            elif cl_mic == 2: 
                tau21 = ((abs(h1).argmax() - abs(h0).argmax())*v/Fs) #calculate the difference between peaks
                tau23 = ((abs(h1).argmax() - abs(h2).argmax())*v/Fs) #in the channel estimates
                tau24 = ((abs(h1).argmax() - abs(h3).argmax())*v/Fs)
                tau25 = ((abs(h1).argmax() - abs(h4).argmax())*v/Fs)

                A = np.array([[p2[0]-p1[0],p2[1]-p1[1],tau21],      
                            [p2[0]-p3[0],p2[1]-p3[1],tau23],
                            [p2[0]-p4[0],p2[1]-p4[1],tau24],
                            [p2[0]-p5[0],p2[1]-p5[1],tau25]])
        
                C = np.array([[0.5*(p2[0]**2-p1[0]**2+p2[1]**2-p1[1]**2+tau21**2)],
                      [0.5*(p2[0]**2-p3[0]**2+p2[1]**2-p3[1]**2+tau23**2)],
                      [0.5*(p2[0]**2-p4[0]**2+p2[1]**2-p4[1]**2+tau24**2)],
                      [0.5*(p2[0]**2-p5[0]**2+p2[1]**2-p5[1]**2+tau25**2)]])

                B = np.linalg.lstsq(A, C, rcond=None)[0][:2].flatten()  #matrix calculation to get coordinates
            elif cl_mic == 3:
                tau31 = ((abs(h2).argmax() - abs(h0).argmax())*v/Fs) #calculate the difference between peaks
                tau32 = ((abs(h2).argmax() - abs(h1).argmax())*v/Fs) #in the channel estimates
                tau34 = ((abs(h2).argmax() - abs(h3).argmax())*v/Fs)
                tau35 = ((abs(h2).argmax() - abs(h4).argmax())*v/Fs)

                A = np.array([[p3[0]-p1[0],p3[1]-p1[1],tau31],      
                      [p3[0]-p2[0],p3[1]-p2[1],tau32],
                      [p3[0]-p4[0],p3[1]-p4[1],tau34],
                      [p3[0]-p5[0],p3[1]-p5[1],tau35]])
        
                C = np.array([[0.5*(p3[0]**2-p1[0]**2+p3[1]**2-p1[1]**2+tau31**2)],
                      [0.5*(p3[0]**2-p2[0]**2+p3[1]**2-p2[1]**2+tau32**2)],
                      [0.5*(p3[0]**2-p4[0]**2+p3[1]**2-p4[1]**2+tau34**2)],
                      [0.5*(p3[0]**2-p5[0]**2+p3[1]**2-p5[1]**2+tau35**2)]])

                B = np.linalg.lstsq(A, C, rcond=None)[0][:2].flatten()  #matrix calculation to get coordinates
            else:
                tau41 = ((abs(h3).argmax() - abs(h0).argmax())*v/Fs) #calculate the difference between peaks
                tau42 = ((abs(h3).argmax() - abs(h1).argmax())*v/Fs) #in the channel estimates
                tau43 = ((abs(h3).argmax() - abs(h2).argmax())*v/Fs)
                tau45 = ((abs(h3).argmax() - abs(h4).argmax())*v/Fs)

                A = np.array([[p4[0]-p1[0],p4[1]-p1[1],tau41],      
                      [p4[0]-p2[0],p4[1]-p2[1],tau42],
                      [p4[0]-p3[0],p4[1]-p3[1],tau43],
                      [p4[0]-p5[0],p4[1]-p5[1],tau45]])
        
                C = np.array([[0.5*(p4[0]**2-p1[0]**2+p4[1]**2-p1[1]**2+tau41**2)],
                      [0.5*(p4[0]**2-p2[0]**2+p4[1]**2-p2[1]**2+tau42**2)],
                      [0.5*(p4[0]**2-p3[0]**2+p4[1]**2-p3[1]**2+tau43**2)],
                      [0.5*(p4[0]**2-p5[0]**2+p4[1]**2-p5[1]**2+tau45**2)]])

                B = np.linalg.lstsq(A, C, rcond=None)[0][:2].flatten()  #matrix calculation to get coordinates
            
            #print(B)
            return B
        d = channel_estimate(x1,x2,x3,x4,x5,y,Fs)       #makes the channel estimates for each mic
        cl_mic = closest_mic(d[0],d[1],d[2],d[3])       #finds the reference mic
        coordinates = matrix_calc(d[0],d[1],d[2],d[3],d[4],cl_mic)  #does the matrix calculation taking into account the reference mic
        return coordinates
    
    def tdoa_input(self,mic1,mic2,mic3,mic4,mic5): 
        b = []
        b = np.stack((mic1, mic2, mic3, mic4, mic5), axis =-1) #takes input arrays and stacks them in a 3d array
                                                               #with each column containing a different microphone
        return b
