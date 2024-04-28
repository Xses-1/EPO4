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
                self.c = int(string[i+4:i+11])

            if string[i] == 'c' and string[i-1] == '_' and string[i-2] == 'f':
                self.f_c = int(string[i+3:i+7])

            if string[i] == 'b' and string[i-1] == '_' and string[i-2] == 'f':
                self.f_b = int(string[i+3:i+7])

            if string[i] == 'r' and string[i-1] == '_' and string[i-2] == 'c':
                self.c_r = int(string[i+3:i+5])

            if string[i] == 'r' and string[i-1] == 'i' and string[i-2] == 'D':
                self.dir = int(string[i+3:i+5])

            if string[i] == 't' and string[i-1] == 'o' and string[i-2] == 'M':
                self.mot = int(string[i+3:i+5])

            if string[i] == 'L' and string[i-1] == ' ' and string[i-2] == '.':
                self.l = int(string[i+2:i+4])

            if string[i] == ' ' and string[i-1] == 'R' and string[i-2] == ' ':
                self.r = int(string[i+1:i+3])

            if string[i] == 't' and string[i-1] == 't' and string[i-2] == 'a':
                self.batt = float(string[i+2:i+5])

            # For now it only logs the sensors l, r, and a timestamp
            now = datetime.now()
            current_time = now.strftime("%M:%S.%f")[:-3]
            with open('../data/report_log.csv', 'w', newline='') as csvfile:
                writer = cs.writer(csvfile)
                writer.writerow(['Time', 'Sensor L', 'Sensor R'])
                writer.writerow([current_time, self.l, self.r])

    def Estop(self):
        self.set_speed(135)
        time.sleep(0.5)
        self.stop()
        self.EstopF = True

    def __del__(self):
        self.serial.close()

