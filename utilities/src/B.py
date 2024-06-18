from A_TDOA import Challenge_A
import numpy as np
import time

if __name__ == '__main__':
    # Define static variables
    target_offset = 0.3      # The distance from the tarrget to still count success
    calibration_delay = 15     # The amount of loop iterations before the TDOA calibration
    size_of_the_field = 4.60    # It's a square
    sleeptime = 0.1

    # Setup function:

    # Ask for the target input
    print("Give First target coordinates in meters separated by a new line")
    print("in following notation: \"X\\nY\", ex. \"0.69\\n4.20\"")
    tX1 = float(input())
    tY1 = float(input())

    print("Give Second target coordinates in meters separated by a new line")
    print("in following notation: \"X\\nY\", ex. \"0.69\\n4.20\"")
    tX2 = float(input())
    tY2 = float(input())

    # For testing the initail position can be typed in
    print("Type in the current position in meters and angle in Radians / (np.pi/2)")
    cX = float(input())
    cY = float(input())
    Theta = np.pi/2*float(input())

    ## Run challenge A for the First time
    cX, cY, Theta = Challenge_A(cX, cY, Theta, tX1, tY1, target_offset, calibration_delay, sleeptime)

    print(cX, cY, Theta)

    ## wait the measuring delay
    time.sleep(10)

    ## Run challenge A the second time
    cX, cY, Theta = Challenge_A(cX, cY, Theta, tX2, tY2, target_offset, calibration_delay, sleeptime)
