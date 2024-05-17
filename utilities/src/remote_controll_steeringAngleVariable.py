#!/bin/python3.10
import keyboard
import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'inc'))
from KITT import KITT

if os.name == 'nt':
    comPort = 'COM7'
else:
    comPort = '/dev/rfcomm0'

steeringAngle = 0

def tick():
    speed,angle = kitt.updateDirectionKeyboard()

    if keyboard.is_pressed('M'):
        global steeringAngle
        if steeringAngle != 50:
            steeringAngle  += 10
        else:
            steeringAngle = 10

        print( f'steeringAngle: {steeringAngle}')

    if angle > 150:
        angle = 150 + steeringAngle
    if angle < 150:
        angle = 150 - steeringAngle

    kitt.set_speed(speed)
    kitt.set_angle(angle)

    
        

if __name__ == '__main__':
    kitt = KITT(comPort)

    while True:
        try:
            tick()

            time.sleep(0.1)

        except KeyboardInterrupt:
            kitt.serial.close()
            sys.exit(1)

    kitt.serial.close()
