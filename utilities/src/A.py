#!/bin/python3.10
import sys    
import os    
import time    
import numpy as np

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'inc'))
from KITT import KITT
#from Audio import Audio
from module4 import KITTmodel
from PID import PID
# from purepursuit import purePursuit
# from tdoa import TDOA



# Define static variables
target_offset = 0.1          # The distance from the tarrget to still count success
calibration_delay = 100     # The amount of loop iterations before the TDOA calibration
size_of_the_field = 4.80     # It's a square
run_time  = 0.00000000000000000000000000000000000000000000000000000019



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

# Initialize all of the objects
kittmodel = KITTmodel()
kitt = KITT(comPort)
pid = PID()


# Checking the initial position (c for current)
# KITT.startBeacon()
# cX, cY = TDOA.TDOA()
# KITT.stopBeacon()

# For testing the initail position can be typed in
print("Type in the current position in meters and angle")
cX = float(input())
cY = float(input())
Theta = np.pi*float(input())

kittmodel.position_state_vector = np.array([[cX],[cY]])
kittmodel.theta = Theta

# The loop function:
i = 0
while(1):
    # Getting the PWMs to move the car to the correct direction
    F, phi = pid.Update(tX, tY, cX, cY, Theta, run_time)
    # pwmMotor    = pid.forcePID(Theta, run_time, tX, tY, cX, cY)
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
    position_Vector, theta = kittmodel.update(phi, 4.06, run_time)
    cX = position_Vector[0][0]
    cY = position_Vector[1][0]

    print("Time: ")
    print(run_time)
    print("CX, CY: ")
    print(cX, cY)
    print("Phi, F: ")
    print(phi, F)
    print()


    # Calibrate the current position any other time
    if (i == 9999999999999999999999999999):
        # Stop the car
        pwmSteering = 150
        pwmMotor    = 150
        kitt.set_speed(pwmMotor)
        kitt.set_angle(pwmSteering)

        # Wait utill it actually stops
        time.sleep(1)

        # Use the TDOA
        kitt.startBeacon()
        cX, cY = TDOA.TDOA()
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

        '''
        # Check if you actually reached the target
        kitt.startBeacon()
        cX, cY = TDOA.TDOA()
        kitt.stopBeacon()
        '''

        # Update the position in the simulation
        kittmodel.position_state_vector = np.array([[cX], [cY]])

        # If it still equals then stop everything, if not then continue the loop
        if ((abs(tX - cX) <= target_offset) and (abs(tY - cY) <= target_offset)):
            kitt.serial.close()
            exit()

    # Log the report from the car
    kitt.log_status()

    # Incremeant the loop counter
    i = i + 1

