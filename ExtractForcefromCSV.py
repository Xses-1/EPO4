import csv
import numpy as np
import matplotlib.pyplot as plt

with open("utilities\\data\\report_log5.csv", "r") as file:
    data = list(csv.reader(file, delimiter=","))

T = []
L = []
R = []
motor = []
for i in data[2:]:
    T.append(i[0])
    L.append(int(i[1]))
    R.append(int(i[2]))
    motor.append(int(i[5]))

velL = np.gradient(L)  
velR = np.gradient(R)

accL = np.gradient(velL)
accR = np.gradient(velR)
print(f"accL = {accL}")
print(f"accR = {accR}")

fig, ax = plt.subplots(2,2)

ax[0][0].plot(L, label='sensorL')
ax[0][0].plot(R, label='sensorR')
ax[0][0].legend()
ax[0][1].plot(velL, label='Velocity L')
ax[0][1].plot(velR, label='Velocity R')
ax[0][1].legend()
ax[1][0].plot(accL, label='acceleration L')
ax[1][0].plot(accR, label='acceleration R')
ax[1][0].legend()
ax[1][1].plot(motor, label='motor')
ax[1][1].legend()

fig.show()

plt.show()