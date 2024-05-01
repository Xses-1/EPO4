#!/bin/python3.10
import serial
import keyboard
import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'inc'))
from KITT import KITT

comPort = '/dev/rfcomm0'
joystickFile = '/dev/uinput'

def Updatekeys():
                #[W,A,S,D,E,Q,X]
    WASD = [0,0,0,0]
    if  kitt.EstopF == True:
        return
    elif keyboard.is_pressed('x'):
        kitt.Estop()

    if keyboard.is_pressed('up'):
        WASD[0] = 1
    else:
        WASD[0] = 0

    if keyboard.is_pressed('left'):
        WASD[1] = 1
    else:
        WASD[1] = 0

    if keyboard.is_pressed('down'):
        WASD[2] = 1
    else:
        WASD[2] = 0

    if keyboard.is_pressed('right'):
        WASD[3] = 1
    else:
        WASD[3] = 0

    if keyboard.is_pressed('e'):
        print('startBeacon')
        kitt.startBeacon()

    if keyboard.is_pressed('q'):
        print('stopBeacon')
        kitt.stopBeacon()

    if keyboard.is_pressed('p'):
        kitt.print_status()

    match WASD:
        ## stop case
        case [0,0,0,0]:
            kitt.stop()

        ## right, no speed
        case [0,0,0,1]:
            kitt.set_angle(100)
            kitt.set_speed(150)
        
        ## straight, backwards
        case [0,0,1,0]:
            kitt.set_angle(150)
            kitt.set_speed(135)
        
        ## right, backwards
        case [0,0,1,1]:
            kitt.set_angle(100)
            kitt.set_speed(140)

        ## left, no speed
        case [0,1,0,0]:
            kitt.set_angle(200)
            kitt.set_speed(150)
        
        ## left, backwards
        case [0,1,1,0]:
            kitt.set_angle(200)
            kitt.set_speed(140)
        
        ## straight, forward
        case [1,0,0,0]:
            kitt.set_angle(150)
            kitt.set_speed(165)

        ## straight, right
        case [1,0,0,1]:
            kitt.set_angle(100)
            kitt.set_speed(160)
        
        ## straight, left
        case [1,1,0,0]:
            kitt.set_angle(200)
            kitt.set_speed(160)
              
        case _:
            kitt.stop()

                                    ## TODO
def updateStick():
    
    #with open(joystickFile, 'r') as joystick:
    #    data = joystick.read()
    ## +- 32767
    xVal = 000 ## This is a test value
    yVal = 000

    x_pwm = 100/65534 * (xVal - 32747) + 100
    y_pwm = 100/65534 * (yVal - 32747) + 100


def updateInput(WhichInput):
    if WhichInput:
        updateStick()
    else:
        Updatekeys()


def tick():
    updateInput(WhichInput)

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
    kitt.setBeacon(carrier_freq = 1000, bit_frequency = 50, repition_count = 2500, code = 0xB00B1E50)

    while True:
        try:
            tick()
            os.system('clear')
            kitt.print_status()
            time.sleep(0.1)

        except KeyboardInterrupt:
            kitt.serial.close()
            break

    kitt.serial.close()
