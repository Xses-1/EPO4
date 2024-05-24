from module4 import KITTmodel
import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0,10,500)
KITT = KITTmodel()
F_m = 10 #N
phi = 20 #degrees

angle = np.concatenate([np.zeros(100), [phi] * 200, np.zeros(200)])

x = []
y = []
for i in range(1,len(t)):
    dt = t[i] - t[i-1]

    position = KITT.update(angle[i], F_m, dt)

    x.append(position[0][0])
    y.append(position[1][0])

    
plt.plot(y,x)
plt.show()
