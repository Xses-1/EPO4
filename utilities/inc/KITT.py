import serial
import keyboard
import sys
import os
import time
import csv
from datetime import datetime

class KITT:
    def __init__(self, port, baudrate=115200):
        self.serial = None
        self.EstopF = False
        self.BeaconFlag = False

        # Those are the extracted data from a report from KITT
        # I am casting to enforce a data type because f*** python philosophy
        self.beacon = False
        self.c = int(0)
        self.f_c = int(0)
        self.f_b = int(0)
        self.c_r = int(0)
        self.dir = int(0)
        self.mot = int(0)
        self.l = int(0)
        self.r = int(0)
        self.batt = float(0)

        self.speed = int(150)
        self.angle = int(150)

        self.history = []

        n = len(os.listdir('../../utilities/data'))
        self.filename = f'../../utilities/data/report_log{n}.csv'

        with open(self.filename, 'x') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Time', 'Sensor L', 'Sensor R', 'Battery V', 'One Direction', 'Motór'])
            
        for i in range(5):
            try:
                self.serial = serial.Serial(port, baudrate, rtscts=True)
                break
            except serial.serialutil.SerialException:
                print(i)
        if self.serial == None:
            raise Exception
        
        self.setBeacon(carrier_freq = 10000, bit_frequency = 5000, repition_count = 2500, code = 0xB00B1E50)
            
        # state variables such as speed, angle are defined here

    def send_command(self, command):
        self.serial.write(command.encode())

    def set_speed(self, speed):
        self.speed = speed
        self.send_command(f'M{speed}\n')

    def set_angle(self, angle):
        self.angle = angle
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
            print('lol')
    
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
        print()

    def log_status(self):
        # This routine splits the string and puts it
        # into voariables that can be then logged
        string = str(self.sitrep())

        i = 0
        while i < len(string):
            if string[i] == ':' and string[i-1] == 'n' and string[i-2] == 'o':
                if (string[i+2] == 'o' and string[i+3] == 'n'):
                    self.beacon = True
                else:
                    self.beacon == False

            if string[i] == ':' and string[i-1] == 'c' and string[i-2] == ' ':
                # This has to converted from hex to dec
                self.c = string[i+4:i+11]

            if string[i] == 'c' and string[i-1] == '_' and string[i-2] == 'f':
                self.f_c = int((string[i+3:i+9].split('\\'))[0])

            if string[i] == 'b' and string[i-1] == '_' and string[i-2] == 'f':
                self.f_b = int((string[i+3:i+9].split('\\'))[0])

            if string[i] == 'r' and string[i-1] == '_' and string[i-2] == 'c':
                self.c_r = int((string[i+3:i+9].split('\\'))[0])

            if string[i] == 'r' and string[i-1] == 'i' and string[i-2] == 'D':
                self.dir = int((string[i+3:i+9].split('\\'))[0])

            if string[i] == 't' and string[i-1] == 'o' and string[i-2] == 'M':
                self.mot = int((string[i+3:i+9].split('\\'))[0])
            
            if string[i] == 'L' and string[i-1] == ' ' and string[i-2] == '.':
                self.l = int((string[i+2:i+9].split(' '))[0])

            if string[i] == ' ' and string[i-1] == 'R' and string[i-2] == ' ':
                self.r = int((string[i+1:i+9].split('\\'))[0])
            
            if string[i] == 't' and string[i-1] == 't' and string[i-2] == 'a':
                self.batt = float((string[i+2:i+9].split(' '))[0])

            i += 1

        # For now it only logs the sensors l, r, and a timestamp
        now = datetime.now()
        current_time = now.strftime("%M:%S.%f")[:-3]
        with open(self.filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([current_time, self.l, self.r, self.batt, self.dir, self.mot])

        l = [self.l, self.r, self.batt, self.dir, self.mot]
        self.history.append(l)
        return l

    def updateDirectionKeyboard(self):
        speed = 150
        angle = 150

        if keyboard.is_pressed('up') or keyboard.is_pressed('w'):
            speed += 15

        if keyboard.is_pressed('left') or keyboard.is_pressed('a'):
            angle += 50

        if keyboard.is_pressed('down') or keyboard.is_pressed('s'):
            speed -= 15

        if keyboard.is_pressed('right') or keyboard.is_pressed('d'):
            angle -= 50

        if keyboard.is_pressed('q'):
            self.startBeacon()

        if keyboard.is_pressed('e'):
            self.stopBeacon()


        return speed, angle

    def updateDirectionStick(self): ## Low level implementation of joysticks TODO
    
        #with open(joystickFile, 'r') as joystick:
        #    data = joystick.read()
        ## +- 32767
        xVal = 000 ## This is a test value
        yVal = 000

        x_pwm = 100/65534 * (xVal - 32747) + 100
        y_pwm = 100/65534 * (yVal - 32747) + 100

    def EstopCondition(): ## Function to check if ESTOP should be initiated automatically // TODO
        return False

    def Estop(self):
        speed = -self.speed + 300
        self.set_speed(speed)
        time.sleep(0.5)
        self.stop()
        self.EstopF = True

'''
    def __del__(self):
        #idk what the hell is that but it's not working so fuck it
        self.serial.close()
'''

