#!/bin/python3.10
import serial
import keyboard
import sys
import os
import time

comPort ='COM7' #COM7 /dev/rfcomm0
joystickFile = '/dev/uinput'

class KITT:
    def __init__(self, port, baudrate=115200):
        self.serial = None
        self.EstopF = False
        self.BeaconFlag = False
        for i in range(3):
            try:
                self.serial = serial.Serial(port, baudrate, rtscts=True)
            except serial.serialutil.SerialException:
                print(i)
        if self.serial == None:
            raise Exception
            
        # state variables such as speed, angle are defined here

    def send_command(self, command):
        self.serial.write(command.encode())

    def set_speed(self, speed):
        self.send_command(f'M{speed}\n')

    def set_angle(self, angle):
        self.send_command(f'D{angle}\n')

    def stop(self):
        self.set_speed(150)
        self.set_angle(150)

    def setBeacon(self, carrier_freq = 1000, bit_frequency = 5000, repition_count = 2500, code = 0xDEADBEEF):
        carrier_freq = carrier_freq.to_bytes(2, byteorder= 'big')
        self.serial.write( b'F' + carrier_freq + b'\n')
        bit_frequency = bit_frequency.to_bytes(2, byteorder= 'big')
        self.serial.write(b'B' + bit_frequency + b'\n')
        repition_count = repition_count.to_bytes(2, byteorder= 'big')
        self.serial.write(b'R' + repition_count + b'\n')
        code = code.to_bytes(4, byteorder= 'big')
        self.serial.write(b'C' + code + b'\n')

    def startBeacon(self):
        if self.BeaconFlag == True:
            return
        else:    
            self.serial.write(b'A1\n')
            self.BeaconFlag = True
    
    def stopBeacon(self):
        if self.BeaconFlag == True:
            self.serial.write(b'A0\n')
            self.BeaconFlag = False
        else:    
            return

    def sitrep(self):
        self.serial.write(b'S\n')
        status = self.serial.read_until(b'\x04')
        return status
    
    def print_status(self):
        string = str(self.sitrep())
        i = 0
        while i < len(string):
            if string[i] == "\\" and string [i+1] == "n":
                print()
                i = i + 1

            else:
                print(string[i], end='')

            i = i + 1
        
        os.system('clear')

    def Estop(self):
        self.set_speed(135)
        time.sleep(0.1)
        self.stop()
        self.EstopF = True

    def __del__(self):
        self.serial.close()


def Updatekeys():
                #[W,A,S,D,E,Q,X]
    WASD = [0,0,0,0]
    if keyboard.is_pressed('x') or kitt.EstopF == True:
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
    
    kitt.print_status()

    kitt.setBeacon(carrier_freq = 1000, bit_frequency = 50, repition_count = 2500, code = 0xB00B1E50)

    while True:
        try:
            tick()
            time.sleep(0.1)
        except KeyboardInterrupt:
            break


    kitt.serial.close()
    
