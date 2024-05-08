import csv
import numpy as np
from matplotlib import pyplot as plt

data = [] 

with open('utilities\\data\\report_log5.csv', newline='') as csvfile:

    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')


    for row in spamreader:
        if row == [] :
            continue
        try:
            data.append(row[0].split(','))
        except ValueError:
            data.append(row[0].split(','))

print(data[1:])

time        =      [float(  i for i in data[1:][0]]
SensorL     =      [float(i) for i in data[1][1:]]
SensorR     =      [float(i) for i in data[2][1:]]
BatteryV    =      [float(i) for i in data[3][1:]]
Direction   =      [float(i) for i in data[4][1:]]
Motor       =      [float(i) for i in data[5][1:]]
print(f'time {time}')
print(SensorL)

gradL = np.gradient(SensorL,2)

print(gradL)

plt.plot(SensorL)
plt.plot(gradL)

plt.show()


