import csv
import numpy as np
import matplotlib.pyplot as plt

with open("utilities\\data\\report_log5.csv", "r") as file:
    data = list(csv.reader(file, delimiter=","))

T = []
L = []
R = []
motor = []
for i in data[20:]:
    T.append(i[0])
    L.append(int(i[1]))
    R.append(int(i[2]))
    motor.append(int(i[5]))

z = []
for i,j in zip(L,R):
    z.append( (i + j)/2 )

window_size = 4
i = 0
# Initialize an empty list to store moving averages
moving_averages = []
 
# Loop through the array to consider
# every window of size 3

while i < len(z) - window_size + 1:
   
    # Store elements from i to i+window_size
    # in list to get the current window
    window = z[i : i + window_size]
 
    # Calculate the average of current window
    window_average = round(sum(window) / window_size, 2)
     
    # Store the average of current
    # window in moving average list
    moving_averages.append(window_average)
     
    # Shift window to right by one position
    i += 1

vel = np.gradient(moving_averages)  


acc = np.gradient(vel)

fig, ax = plt.subplots(2,2)

ax[0][0].plot(L, label='sensorL')
ax[0][0].plot(R, label='sensorR')
ax[0][0].plot(moving_averages, label = 'averaged Z')
ax[0][0].legend()
ax[0][1].plot(vel, label='Velocity average both sensor')
ax[0][1].legend()
ax[1][0].plot(acc, label='acceleration z')
ax[1][0].hlines(0,0,100, colors = 'red')
ax[1][0].legend()
ax[1][1].plot(motor, label='motor')
ax[1][1].legend()

fig.show()

plt.show()