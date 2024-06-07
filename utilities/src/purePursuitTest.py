import numpy as np
import matplotlib.pyplot as plt

from matplotlib.widgets import Button, Slider

import os
import sys
sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'inc'))
from module4 import KITTmodel
from PID import PID
import purepursuit

positionx = -1.0
positiony = 1.0

waittime = 10
movetime = 190
t = np.linspace(0,10,200)
Setpointsx = np.concatenate([np.zeros(waittime), [positionx] * movetime])
Setpointsy = np.concatenate([np.zeros(waittime), [positiony] * movetime])

Pid = PID()
KITT = KITTmodel()
pure = purepursuit.purePursuit()

z = [0]
F = 0.0
phi = 0.0

x = [0.0]
y = [0.0]
Phis = [0]
Thetas = [np.pi/2]

with open('test.txt', 'w') as f:
    f.write(' empty run')

for i in range(1,len(t)):
    dt = t[i] - t[i-1]

    position_Vector, Theta = KITT.update(phi,F,dt)

    x.append(position_Vector[0][0])
    y.append(position_Vector[1][0])
    Thetas.append(Theta)

    _ = pure.purepursuit(x[-1], y[-1], Setpointsx[i], Setpointsy[i], Theta)

    F, phi = Pid.Update(Setpointsx[i], Setpointsy[i], x[-1], y[-1], Theta, dt)

    #print(Pid.angle , '  ', phi)

    Phis.append(phi)

fig, ax = plt.subplots(2,2)
fig.subplots_adjust(bottom=0.2, left = 0.1, top = 0.98, right = 0.99)

line1, = ax[0][0].plot(x, y, lw=2, label = 'car position')
line11, = ax[0][0].plot(Setpointsx, Setpointsy, label = 'car setpoint')
ax[0][0].set_xlabel('X [m]')
ax[0][0].set_ylabel('Y [m]')
ax[0][0].set_ylim(-2,2)
ax[0][0].set_xlim(-2,2)
ax[0][0].legend(loc = 'upper right')

line2, = ax[0][1].plot(t, Phis, lw=2, label = 'wheel Angle')
line22 = ax[0][1].set_ylabel('wheel angle [Deg]')
ax[0][1].set_ylim(-0.8,0.8)
ax[0][1].set_xlabel('time [s]')
ax[0][1].legend()


line3, = ax[1][0].plot(t, Thetas, lw=2, label = 'Thetas')
line33, = ax[1][0].plot(t,(np.concatenate([[0.0] * waittime, [45.0] * movetime])), label = 'theta setpoint')
ax[1][0].set_ylabel('Theta [deg]')
ax[1][0].set_xlabel('time [s]')
ax[1][0].set_ylim(-1,np.pi)
ax[1][0].legend(loc = 'upper right')

line4, = ax[1][1].plot(t, x, lw=2, label = 'x position')
line44, = ax[1][1].plot(t,Setpointsx, label = 'x setpoint')
ax[1][1].set_ylabel('x position [m]')
ax[1][1].set_xlabel('time [s]')
ax[1][1].set_ylim(-2,2)
ax[1][1].legend(loc = 'upper right')

plt.show()