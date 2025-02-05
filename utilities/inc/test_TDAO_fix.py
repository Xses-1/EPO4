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
    
    def localization_mic1(self, x1,x2,x3,x4,x5, y, Fs):
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

        tau12 = ((abs(h0).argmax() - abs(h1).argmax())*v/Fs) #calculate the difference between peaks
        tau14 = ((abs(h0).argmax() - abs(h3).argmax())*v/Fs) #in the channel estimates
        tau13 = ((abs(h0).argmax() - abs(h2).argmax())*v/Fs)
        tau15 = ((abs(h0).argmax() - abs(h4).argmax())*v/Fs)

        p1 = np.array([0, 0])       #define microphone positions
        p2 = np.array([0, 4.60])
        p3 = np.array([4.60, 4.60])
        p4 = np.array([4.60, 0])
        p5 = np.array([0, 2.60])
        
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
    
    def localization_mic2(self, x1,x2,x3,x4,x5, y, Fs):
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

        tau21 = ((abs(h1).argmax() - abs(h0).argmax())*v/Fs) #calculate the difference between peaks
        tau23 = ((abs(h1).argmax() - abs(h2).argmax())*v/Fs) #in the channel estimates
        tau24 = ((abs(h1).argmax() - abs(h3).argmax())*v/Fs)
        tau25 = ((abs(h1).argmax() - abs(h4).argmax())*v/Fs)

        p1 = np.array([0, 0])       #define microphone positions
        p2 = np.array([0, 4.60])
        p3 = np.array([4.60, 4.60])
        p4 = np.array([4.60, 0])
        p5 = np.array([0, 2.30])
        
        A = np.array([[p2[0]-p1[0],p2[1]-p1[1],tau21],      
                      [p2[0]-p3[0],p2[1]-p3[1],tau23],
                      [p2[0]-p4[0],p2[1]-p4[1],tau24],
                      [p2[0]-p5[0],p2[1]-p5[1],tau25]])
        
        C = np.array([[0.5*(p2[0]**2-p1[0]**2+p2[1]**2-p1[1]**2+tau21**2)],
                      [0.5*(p2[0]**2-p3[0]**2+p2[1]**2-p3[1]**2+tau23**2)],
                      [0.5*(p2[0]**2-p4[0]**2+p2[1]**2-p4[1]**2+tau24**2)],
                      [0.5*(p2[0]**2-p5[0]**2+p2[1]**2-p5[1]**2+tau25**2)]])

        B = np.linalg.lstsq(A, C, rcond=None)[0][:2].flatten()  #matrix calculation to get coordinates

        #print(B)
        return B

    def localization_mic3(self, x1,x2,x3,x4,x5, y, Fs):
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

        tau31 = ((abs(h2).argmax() - abs(h0).argmax())*v/Fs) #calculate the difference between peaks
        tau32 = ((abs(h2).argmax() - abs(h1).argmax())*v/Fs) #in the channel estimates
        tau34 = ((abs(h2).argmax() - abs(h3).argmax())*v/Fs)
        tau35 = ((abs(h2).argmax() - abs(h4).argmax())*v/Fs)

        p1 = np.array([0, 0])       #define microphone positions
        p2 = np.array([0, 4.60])
        p3 = np.array([4.60, 4.60])
        p4 = np.array([4.60, 0])
        p5 = np.array([0, 2.30])
        
        A = np.array([[p3[0]-p1[0],p3[1]-p1[1],tau31],      
                      [p3[0]-p2[0],p3[1]-p2[1],tau32],
                      [p3[0]-p4[0],p3[1]-p4[1],tau34],
                      [p3[0]-p5[0],p3[1]-p5[1],tau35]])
        
        C = np.array([[0.5*(p3[0]**2-p1[0]**2+p3[1]**2-p1[1]**2+tau31**2)],
                      [0.5*(p3[0]**2-p2[0]**2+p3[1]**2-p2[1]**2+tau32**2)],
                      [0.5*(p3[0]**2-p4[0]**2+p3[1]**2-p4[1]**2+tau34**2)],
                      [0.5*(p3[0]**2-p5[0]**2+p3[1]**2-p5[1]**2+tau35**2)]])

        B = np.linalg.lstsq(A, C, rcond=None)[0][:2].flatten()  #matrix calculation to get coordinates

        #print(B)
        return B
    
    def localization_mic4(self, x1,x2,x3,x4,x5, y, Fs):
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

        tau41 = ((abs(h3).argmax() - abs(h0).argmax())*v/Fs) #calculate the difference between peaks
        tau42 = ((abs(h3).argmax() - abs(h1).argmax())*v/Fs) #in the channel estimates
        tau43 = ((abs(h3).argmax() - abs(h2).argmax())*v/Fs)
        tau45 = ((abs(h3).argmax() - abs(h4).argmax())*v/Fs)

        p1 = np.array([0, 0])       #define microphone positions
        p2 = np.array([0, 4.60])
        p3 = np.array([4.60, 4.60])
        p4 = np.array([4.60, 0])
        p5 = np.array([0, 2.30])
        
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
    
    
    def closest_mic(h0,h1,h2,h3):
        distances = np.array([[abs(h0).argmax()], [abs(h1).argmax()], [abs(h2).argmax()], [abs(h3).argmax()]])
        min_value = min(distances)
        min_pos = np.argmin(distances) + 1
        print(min_value)
        print(min_pos)
        return min_pos
    
    def select_closest_mic(min_pos):
        if min_pos == 1:
            closest_mic = 1
        
        elif min_pos == 2:
            closest_mic = 2
        
        elif min_pos == 3:
            closest_mic = 3
        
        else:
            closest_mic = 4
        
        return closest_mic
    
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
    
#    def pick_locatlization(the_closest_mic):
#        if the_closest_mic == 1:
            
#        elif the_closest_mic == 2:

#        elif the_closest_mic == 3:

#        else:
#            
        





        
