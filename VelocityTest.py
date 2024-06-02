from module4 import KITTmodel
import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0,20,400)
KITT = KITTmodel()
F_m = 1 #N

F = np.concatenate([[F_m] * 400])

V = []

for i in range(1,len(t)):
    dt = t[i] - t[i-1]
    v = KITT.velocity_state(F[i], dt)

    V.append(v)

plt.plot(t[:-1],V)

plt.show()