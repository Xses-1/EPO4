#!/bin/python3.10
import keyboard
import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'inc'))
from KITT import KITT

#comPort = 'COM10'
comPort = '/dev/rfcomm0'
joystickFile = '/dev/uinput'

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
            os.system('clear')
            kitt.print_status()
            kitt.log_status()
            time.sleep(0.1)

        except KeyboardInterrupt:
            kitt.serial.close()
            break

    kitt.serial.close()
