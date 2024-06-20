import matplotlib.style
import pylab as plt
import numpy as np
import matplotlib

class GUI:
    def __init__(self, Startx, Starty, startTheta, setpointx, setpointy, sleeptime = 0.1):
        self.sleeptime = sleeptime
        matplotlib.use('TkAgg')
        plt.style.use('classic')
        plt.figure(figsize=(15.08,9.01))
        plt.ion()
        plt.xlim(-0.5,5)
        plt.ylim(-0.5,5)
        self.CarPosition = plt.scatter(Startx, Starty, color = 'blue')
        dx = np.cos(startTheta) * 0.2
        dy = np.sin(startTheta) * 0.2
        self.CarVector = plt.arrow(Startx, Starty, dx, dy, head_width = 0.1,
                                                            width = 0.02,
                                                            ec ='green')

        self.setpoint = plt.scatter(setpointx, setpointy, color = 'red')
        plt.draw()

        plt.pause(0.5)

    def update(self, carx, cary, carTheta, setpointx, setpointy):
        plt.clf()
        plt.xlim(-0.5,5)
        plt.ylim(-0.5,5)
        self.CarPosition = plt.scatter(carx, cary)
        dx = np.cos(carTheta) * 0.2
        dy = np.sin(carTheta) * 0.2
        self.CarVector = plt.arrow(carx, cary, dx, dy, head_width = 0.1,
                                                            width = 0.02,
                                                            ec ='green')

        self.setpoint = plt.scatter(setpointx, setpointy, color = 'red')

        plt.draw()
        plt.pause(self.sleeptime)

        
