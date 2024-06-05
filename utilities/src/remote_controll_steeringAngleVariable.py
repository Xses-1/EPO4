#!/bin/python3.10
import keyboard
import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'inc'))
from KITT import KITT

if os.name == 'nt':
    comPort = 'COM5'
else:
    comPort = '/dev/rfcomm0'

deltangle = 0

def tick():
    speed,angle = kitt.updateDirectionKeyboard()

    if keyboard.is_pressed('M'):
        global deltaspeed
        if deltaspeed != 15:
            deltaspeed  += 5
        else:
            deltaspeed = 5

        print( f'deltaspeed: {deltaspeed}')

    if speed > 150:
        speed = 150 + deltaspeed
    if speed < 150:
        speed = 150 - deltaspeed
        global deltangle
        if deltangle != 50:
            deltangle  += 10
        else:
            deltangle = 10

        print( f'deltangle: {deltangle}')

    if angle > 150:
        angle = 150 + deltangle
    if angle < 150:
        angle = 150 - deltangle

    kitt.set_speed(speed)
    kitt.set_angle(angle)

    
        

if __name__ == '__main__':
    kitt = KITT(comPort)

    while True:
        try:
            tick()
            kitt.log_status()
            kitt.log_status()

            time.sleep(0.1)

        except KeyboardInterrupt:
            kitt.serial.close()
            sys.exit(1)

    kitt.serial.close()
