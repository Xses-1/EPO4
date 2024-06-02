from module4 import KITTmodel
from PID import PID
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.widgets import Button, Slider

positionx = 1.0
positiony = 1.0
currentAngle = 90.0

t = np.linspace(0,40,2000)
Setpointsx = np.concatenate([np.zeros(100), [positionx] * 1900])
Setpointsy = np.concatenate([np.zeros(100), [positiony] * 1900])

Pid = PID()
KITT = KITTmodel()

z = [0]
F = 0.0
phi = 0.0

x = [0.0]
y = [0.0]
angle = [90.0]
Phis = [0]
Thetas = [0]

for i in range(1,len(t)):
    dt = t[i] - t[i-1]

    position_Vector, Theta = KITT.update(phi,F,dt)

    x.append(position_Vector[0][0])
    y.append(position_Vector[1][0])
    

    F,phi = Pid.Update(Setpointsx[i], Setpointsy[i], x[-1], y[-1], Theta, dt)

    Phis.append(phi)
    Thetas.append(Theta)
    
fig,ax = plt.subplots(2,2)


ax[0][0].plot(y,x, label = 'car position')
ax[0][0].plot(Setpointsy, Setpointsx, label = 'car setpoint')
ax[0][0].set_xlabel('X [m]')
ax[0][0].set_ylabel('Y [m]')
ax[0][0].legend(loc = 'upper right')

ax[0][1].plot(t,Phis, label = 'wheel Angle')
ax[0][1].set_ylabel('wheel angle [Deg]')
ax[0][1].set_xlabel('time [s]')
ax[0][1].legend()


ax[1][0].plot(t,y, label = 'y position')
ax[1][0].plot(t,Setpointsy, label = 'y setpoint')
ax[1][0].set_ylabel('y postion [m]')
ax[1][0].set_xlabel('time [s]')
ax[1][0].legend(loc = 'upper right')

ax[1][1].plot(t,Thetas, label = 'thetas')
ax[1][1].plot(t,Setpointsx, label = 'x setpoint')
ax[1][1].set_ylabel('x position [m]')
ax[1][1].set_xlabel('time [s]')
ax[1][1].legend(loc = 'upper right')

plt.show()