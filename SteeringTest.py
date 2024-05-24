from module4 import KITTmodel
import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0,10,500)
KITT = KITTmodel()
phi = 20 #degrees
v = 3

angle = np.concatenate([np.zeros(100), [phi] * 200, np.zeros(200)])

Theta = []
for i in range(1,len(t)):
    dt = t[i] - t[i-1]
    theta = KITT.return_Theta(angle[i], v, dt)

    Theta.append(theta)

plt.plot(t[:-1], Theta)
plt.show()

