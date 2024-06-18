#!/bin/python3.10

import numpy as np



def Challenge_A(cX, cY, Theta, tX, tY, target_offset, calibration_delay, sleeptime):
    import sys    
    import os    
    import time    
    from pathlib import Path

    sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'inc'))
    from wavaudioread import wavaudioread
    from KITT import KITT
    from Audio import Audio
    from module4 import KITTmodel
    from PID import PID
    from var_ref_tdoa import TDOA
    from GUI import GUI

    run_time  = 19e-127         # 0 but not 0 so the divide by 0 does not break

    #Check if the target is valid
    if ((tX > size_of_the_field) or (tY > size_of_the_field)):
        print("Invalid target, BYE! 😠")
        exit() 

    # Checiking the os and connecting to the port
    if os.name == 'nt':
        comPort = 'COM5'
    else:
        comPort = '/dev/rfcomm0'


    # Initializing the mics and refrence files
    mics = Audio()
    Fs = 44100
    N = Fs * 1
    data = mics.sample(N)
    samples = mics.split_data(data)



    # Initialize all of the objects
    kittmodel = KITTmodel()
    kitt = KITT(comPort)
    pid = PID()
    T = TDOA()


    #Using reference recordings from all microphones
    y = T.tdoa_input(samples[0], samples[1], samples[2], samples[3], samples[4])
    root_folder = Path("IntegrationTest.py").resolve().parent
    x1 = wavaudioread(root_folder / "utilities/data/Reference1.wav", Fs)
    x2 = wavaudioread(root_folder / "utilities/data/Reference2.wav", Fs)
    x3 = wavaudioread(root_folder / "utilities/data/Reference3.wav", Fs)
    x4 = wavaudioread(root_folder / "utilities/data/Reference4.wav", Fs)
    x5 = wavaudioread(root_folder / "utilities/data/Reference5.wav", Fs)


    kittmodel.position_state_vector = np.array([[cX],[cY]])
    kittmodel.theta = Theta

    # Checking the initial position (c for current)
    kitt.startBeacon()
    time.sleep(0.5)
    data = mics.sample(N)
    samples = mics.split_data(data)
    y = T.tdoa_input(samples[0], samples[1], samples[2], samples[3], samples[4])
    pos = T.localization(x1,x2,x3,x4,x5, y, Fs)
    print(pos)
    kitt.stopBeacon()

    print(cX, cY)

    G = GUI(cX, cY,Theta, tX, tY, sleeptime = sleeptime)

    # The loop function:
    i = 0
    while(1):

        if(i < calibration_delay - 5):
            # Getting the PWMs to move the car to the correct direction
            F, phi = pid.Update(tX, tY, cX, cY, Theta, run_time)
            print(f'F: {F}')
            pwmMotor    = pid.ForcetoPWM(F)
            pwmSteering = pid.RadiansToPWM(phi)

            #pwmMotor    = 160 # Can be fixed for testing
            #F = 4.992

            # Get the time when the car started to move
            time_old = time.monotonic()

            # Transmitting the PWMs to the car and making it move
            kitt.set_speed(pwmMotor)
            kitt.set_angle(pwmSteering)

            #GUI update, aslo includes the sleep for movement
            G.update(cX, cY, Theta, tX, tY)
            #time.sleep(0.1)

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
        if (i == calibration_delay):
            # Stop the car
            #pwmSteering = 150
            pwmMotor    = 150
            F = 0
            kitt.set_speed(pwmMotor)
            #kitt.set_angle(pwmSteering)

            # Wait utill it actually stops
            time.sleep(1)

            # Use the TDOA
            kitt.startBeacon()
            time.sleep(0.5)
            data = mics.sample(N)
            samples = mics.split_data(data)
            y = T.tdoa_input(samples[0], samples[1], samples[2], samples[3], samples[4])
            pos = T.localization(x1,x2,x3,x4,x5, y, Fs)
            cX = pos[0]
            cY = pos[1]
            print(f'TDOA POS{cX, cY}')
            kitt.stopBeacon()

            # Update the position in the simulation and restart the models since the car waited to stop
            #pid = PID()
            kittmodel = KITTmodel()
            kittmodel.position_state_vector = np.array([[cX],[cY]])
            kittmodel.theta = Theta

            i -= calibration_delay


        # Check if the target was reached with some margin
        if ((abs(tX - cX) <= target_offset) and (abs(tY - cY) <= target_offset)):
            # Stop the car
            pwmSteering = 150
            pwmMotor    = 150
            F = 0
            kitt.set_speed(pwmMotor)
            kitt.set_angle(pwmSteering)

            # Wait untill it actually stops
            time.sleep(1)

            # Check if you actually reached the target
            kitt.startBeacon()
            time.sleep(0.5)
            data = mics.sample(N)
            samples = mics.split_data(data)
            y = T.tdoa_input(samples[0], samples[1], samples[2], samples[3], samples[4])
            pos = T.localization(x1,x2,x3,x4,x5, y, Fs)
            cX = pos[0]
            cY = pos[1]
            print(f'TDOA POS{cX, cY}')
            kitt.stopBeacon()

            # Update the position in the simulation
            kittmodel.position_state_vector = np.array([[cX], [cY]])

            # If it still equals then stop everything, if not then continue the loop
            if ((abs(tX - cX) <= target_offset) and (abs(tY - cY) <= target_offset)):
                # Print the values that can be used to run the code again for challange B
                print(cX, cY, Theta)

                kitt.serial.close()
                break

        # Log the report from the car
        # kitt.log_status()

        # Incremeant the loop counter

        i = i + 1
    
    return cX, cY, Theta
    

if __name__ == '__main__':
    # Define static variables
    target_offset = 0.3      # The distance from the tarrget to still count success
    calibration_delay = 15     # The amount of loop iterations before the TDOA calibration
    size_of_the_field = 4.60    # It's a square
    sleeptime = 0.1

    # Setup function:

    # Ask for the target input
    print("Give target coordinates in meters separated by a new line")
    print("in following notation: \"X\\nY\", ex. \"0.69\\n4.20\"")
    tX = float(input())
    tY = float(input())

    # For testing the initail position can be typed in
    print("Type in the current position in meters and angle in Radians / (np.pi/2)")
    cX = float(input())
    cY = float(input())
    Theta = np.pi/2*float(input())

    cX, cY, Theta = Challenge_A(cX, cY, Theta, tX, tY, target_offset, calibration_delay, sleeptime)

    print(cX, cY, Theta)
