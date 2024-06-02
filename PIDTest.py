from module4 import KITTmodel
from PID import PID
import numpy as np
import matplotlib.pyplot as plt
positionx = 1
positiony = 0.0
currentAngle = 0.0

t = np.linspace(0,40,2000)
positionx = np.concatenate([np.zeros(100), [positionx] * 1900])

Pid = PID()
KITT = KITTmodel()

z = [0]
F = 0
for i in range(1,len(t)):
    dt = t[i] - t[i-1]

    v = KITT.velocity_state(F, dt)
    z.append(z[-1] + (v * dt))


    deltaP, deltaTheta = Pid.CalculateErrors(positionx[i], positiony, z[-1], positiony, currentAngle)

    F = Pid.calculateForce(deltaP, dt)

plt.plot(t, z)
plt.vlines(2,0,1,colors = 'red')
plt.show()



