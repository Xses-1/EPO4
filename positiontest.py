from module4 import KITTmodel
import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0,5,50)
KITT = KITTmodel()
F_m = 1.47 #N
phi = 25 #degrees
N_0 = 0

F = np.concatenate([[F_m] * 40, [N_0] * 10])
angle = np.concatenate([[N_0] * 20, [phi] * 20, [N_0] *10])

x = []
y = []
for i in range(1,len(t)):
    dt = t[i] - t[i-1]

    position = KITT.update(angle[i], F[i], dt)

    x.append(position[0][0])
    y.append(position[1][0])

plt.plot(y,x)
plt.show()
