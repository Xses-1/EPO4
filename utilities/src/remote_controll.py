#!/bin/python3.10
import keyboard
import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'inc'))
from KITT import KITT

if os.name == 'nt':
    comPort = 'COM13'
else:
    comPort = '/dev/rfcomm0'

def tick():
    speed,angle = kitt.updateDirectionKeyboard()

    kitt.set_speed(speed)
    kitt.set_angle(angle)

def alt_c():
    global WhichInput
    WhichInput = not WhichInput
    if WhichInput:
        print('joystick Selected')        
    else:
        print('keyboard Selected')
        
WhichInput = False

if __name__ == '__main__':
    keyboard.add_hotkey('alt+c', alt_c)
    
    kitt = KITT(comPort)

    while True:
        try:
            tick()
            #kitt.print_status()
            kitt.log_status()

        except KeyboardInterrupt:
            kitt.serial.close()
            break

    kitt.serial.close()
