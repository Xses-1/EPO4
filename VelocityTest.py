from module4 import KITTmodel
import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0,10,500)
KITT = KITTmodel()
F_m = 18 #N

V = []

for i in range(1,len(t)):
    dt = t[i] - t[i-1]
    v = KITT.velocity_state(F_m, dt)

    V.append(v)

plt.plot(t[:-1],V)

plt.show()