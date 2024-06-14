#!/bin/python3.10
import sys    
import os    
import time    
import numpy as np
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'inc'))
from wavaudioread import wavaudioread
from KITT import KITT
from Audio import Audio
from module4 import KITTmodel
from PID import PID
from var_ref_tdoa import TDOA



# Define static variables
target_offset = 0.6         # The distance from the tarrget to still count success
calibration_delay = 100     # The amount of loop iterations before the TDOA calibration
size_of_the_field = 4.60    # It's a square
run_time  = 19e-127         # 0 but not 0 so the divide by 0 does not break



# Setup function:

# Ask for the target input
print("Give target coordinates in meters separated by a new line")
print("in following notation: \"X\\nY\", ex. \"0.69\\n4.20\"")
tX = float(input())
tY = float(input())

# Check if the target is valid
if ((tX > size_of_the_field) or (tY > size_of_the_field)):
    print("Invalid target, BYE! 😠")
    exit()


# Checiking the os and connecting to the port
if os.name == 'nt':
    comPort = 'COM22'
else:
    comPort = '/dev/rfcomm0'


# Initializing the mics and refrence files
mics = Audio()
N = 44100 * 1
data = mics.sample(N)
samples = mics.split_data(data)
Fs = 44100


# Initialize all of the objects
kittmodel = KITTmodel()
kitt = KITT(comPort)
pid = PID()
mics = Audio()
T = TDOA()


#Using reference recordings from all microphones
y = T.tdoa_input(samples[0], samples[1], samples[2], samples[3], samples[4])
root_folder = Path("IntegrationTest.py").resolve().parent
x1 = wavaudioread(root_folder / "utilities/data/Reference1.wav", Fs)
x2 = wavaudioread(root_folder / "utilities/data/Reference2.wav", Fs)
x3 = wavaudioread(root_folder / "utilities/data/Reference3.wav", Fs)
x4 = wavaudioread(root_folder / "utilities/data/Reference4.wav", Fs)
x5 = wavaudioread(root_folder / "utilities/data/Reference5.wav", Fs)


# Checking the initial position (c for current)
KITT.startBeacon()
cX = T.localization(x1,x2,x3,x4,x5, y, Fs)[0]
cY = T.localization(x1,x2,x3,x4,x5, y, Fs)[1]
KITT.stopBeacon()

# For testing the initail position can be typed in
print("Type in the current position in meters and angle")
cX = float(input())
cY = float(input())
Theta = np.pi/2*float(input())

kittmodel.position_state_vector = np.array([[cX],[cY]])
kittmodel.theta = Theta

# The loop function:
i = 0
while(1):
    # Getting the PWMs to move the car to the correct direction
    F, phi = pid.Update(tX, tY, cX, cY, Theta, run_time)
    #pwmMotor    = pid.ForceToPWM(F)
    pwmSteering = pid.RadiansToPWM(phi)
    pwmMotor    = 160 # Can be fixed for testing

    # Get the time when the car started to move
    time_old = time.monotonic()

    # Transmitting the PWMs to the car and making it move
    kitt.set_speed(pwmMotor)
    kitt.set_angle(pwmSteering)

    # Let the car move for some time
    time.sleep(0.1)

    # Calcualting the current position of the car with the model
    run_time = time.monotonic() - time_old
    position_Vector, Theta = kittmodel.update(phi, 4.06, run_time)
    cX = position_Vector[0][0]
    cY = position_Vector[1][0]

    # Testing and troubleshooting
    '''
    print("Time: ")
    print(run_time)
    print("CX, CY: ")
    print(cX, cY)
    print("Phi, F: ")
    print(phi, F)
    '''
    print("PMWs: ")
    print(pwmSteering, pwmMotor)
    print()


    # Calibrate the current position any other time
    if (i == 100):
        # Stop the car
        pwmSteering = 150
        pwmMotor    = 150
        kitt.set_speed(pwmMotor)
        kitt.set_angle(pwmSteering)

        # Wait utill it actually stops
        time.sleep(1)

        # Use the TDOA
        kitt.startBeacon()
        cX = T.localization(x1,x2,x3,x4,x5, y, Fs)[0]
        cY = T.localization(x1,x2,x3,x4,x5, y, Fs)[1]
        kitt.stopBeacon()

        # Update the position in the simulation
        KITTmodel.position_state_vector = np.array([[cX], [cY]])

    
    # Check if the target was reached with some margin
    if ((abs(tX - cX) <= target_offset) and (abs(tY - cY) <= target_offset)):
        # Stop the car
        pwmSteering = 150
        pwmMotor    = 150
        kitt.set_speed(pwmMotor)
        kitt.set_angle(pwmSteering)

        # Wait untill it actually stops
        time.sleep(1)

        # Check if you actually reached the target
        kitt.startBeacon()
        cX = T.localization(x1,x2,x3,x4,x5, y, Fs)[0]
        cY = T.localization(x1,x2,x3,x4,x5, y, Fs)[1]
        kitt.stopBeacon()

        # Update the position in the simulation
        kittmodel.position_state_vector = np.array([[cX], [cY]])

        # If it still equals then stop everything, if not then continue the loop
        if ((abs(tX - cX) <= target_offset) and (abs(tY - cY) <= target_offset)):
            # Print the values that can be used to run the code again for challange B
            print(cX, cY, Theta)

            kitt.serial.close()
            exit()

    # Log the report from the car
    # kitt.log_status()

    # Incremeant the loop counter
    i = i + 1
