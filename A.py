#!/bin/python3.10
import sys    
import os    
import time    

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'utilities/inc'))    
from KITT import KITT
from Audio import Audio
from module4 import KITTmodel
from PID import PID
from purepursuit import purePursuit
from tdoa import TDOA



# Define static variables
target_offset = 10          # The distance from the tarrget to still count success
calibration_delay = 100     # The amount of loop iterations before the TDOA calibration
size_of_the_field = 4.80     # It's a square



# Setup function:

# Ask for the target input
print("Give target coordinates in meters separated by a new line")
print("in following notation: \"X\\nY\", ex. \"0.69\\n4.20\"")
tX = int(input())
tY = int(input())

# Check if the target is valid
if ((tX > size_of_the_field) or (tY > size_of_the_field)):
    print("Invalid target, BYE! 😠")
    exit()


# Checiking the os and connecting to the port
if os.name == 'nt':    
    comPort = 'COM22'    
else:    
    comPort = '/dev/rfcomm0'

kitt = KITT(comPort)


# Checking the initial position (c for current)
# KITT.startBeacon()
# cX, cY = TDOA.TDOA()
# KITT.stopBeacon()

# For testing the initail position can be typed in
print("Type in the current position in meters")
cX = float(input())
cY = float(input())



# The loop function:
i = 0
while(1):
    # Getting the PWMs to move the car to the correct direction
    pwmSteering = purePursuit.steering(theta, run_time, tX, tY, cX, cY)
    pwmMotor    = PID.forcePID(theta, run_time, tX, tY, cX, cY)
    pwmMotor    = 160 # Can be fixed for testing

    # Get the time when the car started to move
    time_old = monotonic()

    # Transmitting the PWMs to the car and making it move
    KITT.set_spped(pwmMotor)
    KITT.set_angle(pwmSteering)

    # Let the car move for some time
    time.sleep(0.5)

    # Calcualting the current position of the car with the model
    run_time = time.monotonic() - time_old
    cX, cY, theta = KITTmodel.position(run_time, pwmMotor, pwmSteering)

    # Calibrate the current position any other time
    if (i == 100):
        # Stop the car
        pwmSteering = 150
        pwmMotor    = 150
        KITT.set_spped(pwmMotor)
        KITT.set_angle(pwmSteering)

        # Wait utill it actually stops
        time.sleep(1)

        # Use the TDOA
        KITT.startBeacon()
        cX, cY = TDOA.TDOA()
        KITT.stopBeacon()

        # Update the position in the simulation
        KITTmodel.position_state_vector = np.array([[cX], [cY]])

    
    # Check if the target was reached with some margin
    if ((abs(tX - cX) <= target_offset) and (abs(tY - cY) <= target_offset)):
        # Stop the car
        pwmSteering = 150
        pwmMotor    = 150
        KITT.set_spped(pwmMotor)
        KITT.set_angle(pwmSteering)

        # Wait untill it actually stops
        time.sleep(1)

        # Check if you actually reached the target
        KITT.startBeacon()
        cX, cY = TDOA.TDOA()
        KITT.stopBeacon()

        # Update the position in the simulation
        KITTmodel.position_state_vector = np.array([[cX], [cY]])

        # If it still equals then stop everything, if not then continue the loop
        if ((abs(tX - cX) <= target_offset) and (abs(tY - cY) <= target_offset)):
            KITT.serial.close()
            exit()

    # Log the report from the car
    KITT.log_status()

    # Incremeant the loop counter
    i = i + 1

