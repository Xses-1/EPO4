import os
import sys
sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'inc'))
from module4 import KITTmodel
import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0,20,400)
KITT = KITTmodel()
F_m = 8.91 #N

F = np.concatenate([[F_m] * 300, [0] * 100])

V = []
z = [0]

for i in range(1,len(t)):
    dt = t[i] - t[i-1]
    v = KITT.velocity_state(F[i], dt)
    V.append(v)

    z.append(z[-1] + v * dt)

plt.plot(t,z)
plt.hlines(z[200], 0,20, colors = 'red')

print(z[300], z[399],  z[399]- z[300])
print(V[300])
plt.show()