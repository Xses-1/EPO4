import pylab as plt
import numpy as np
import matplotlib

class GUI:
    def __init__(self, Startx, Starty, startTheta, setpointx, setpointy, sleeptime = 0.1):
        self.sleeptime = sleeptime
        matplotlib.use('TkAgg')
        plt.ion()
        plt.xlim(-0.5,5)
        plt.ylim(-0.5,5)
        self.CarPosition = plt.scatter(Startx, Starty, color = 'blue')
        dx = np.cos(startTheta) * 0.4
        dy = np.sin(startTheta) * 0.4
        self.CarVector = plt.arrow(Startx, Starty, dx, dy, head_width = 0.2,
                                                            width = 0.05,
                                                            ec ='green')

        self.setpoint = plt.scatter(setpointx, setpointy, color = 'red')
        plt.draw()

        plt.pause(2)

    def update(self, carx, cary, carTheta, setpointx, setpointy):
        plt.clf()
        plt.xlim(-0.5,5)
        plt.ylim(-0.5,5)
        self.CarPosition = plt.scatter(carx, cary)
        dx = np.cos(carTheta) * 0.4
        dy = np.sin(carTheta) * 0.4
        self.CarVector = plt.arrow(carx, cary, dx, dy, head_width = 0.2,
                                                            width = 0.05,
                                                            ec ='green')

        self.setpoint = plt.scatter(setpointx, setpointy, color = 'red')

        plt.draw()
        plt.pause(self.sleeptime)