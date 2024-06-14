import os
import sys
sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'inc'))
from module4 import KITTmodel
import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0,10,100)
KITT = KITTmodel()
F_m = 4.06 #N
phi = 20 #degrees
N_0 = 0

F = np.concatenate([[F_m] * 40, [N_0] * 60])
angle = np.concatenate([[N_0] * 20, [phi] * 20, [N_0] *60])

x = []
y = []
for i in range(1,len(t)):
    dt = t[i] - t[i-1]

    position, theta = KITT.update(angle[i], F[i], dt)

    print(theta)

    x.append(position[0][0])
    y.append(position[1][0])
    
plt.plot(x,y)
plt.show()
