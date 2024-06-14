import serial
import keyboard
import sys
import os
import time
import csv
from datetime import datetime
import subprocess
import threading
import queue 
import collections

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
        self.time_old = time.monotonic()
        self.time_new = time.monotonic() 
        self.l = int(0)
        self.l_old = int(0)
        self.r = int(0)
        self.r_old = int(0)
        self.batt = float(0)

        self.speed = int(150)
        self.angle = int(150)

        self.history = []

        if os.name == 'nt':
            n = len(os.listdir('utilities/data'))
            self.filename = f'utilities/data/report_log{n}.csv'
        else:
            n = len(os.listdir('../../utilities/data'))
            self.filename = f'../../utilities/data/report_log{n}.csv'

        with open(self.filename, 'x') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Time', 'Sensor_L', 'Sensor_R', 'Battery_V', 'One_Direction', 'Motór'])
            
        for i in range(5):
            try:
                self.serial = serial.Serial(port, baudrate, rtscts=True)
                break
            except serial.serialutil.SerialException:
                print(i)
        if self.serial == None:
            raise Exception
        
        self.setBeacon(carrier_freq = 5000, bit_frequency = 5000, repition_count = 2500, code = 0xB00B1E50)
            
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

    def setFreq(self, freq):
        freq = freq.to_bytes(2, byteorder= 'big')
        self.serial.write( b'F' + freq + b'\n')

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
                self.l_old = self.l
                self.time_old = self.time_new
                self.l = int((string[i+2:i+9].split(' '))[0])
                self.time_new = time.monotonic() 

            if string[i] == ' ' and string[i-1] == 'R' and string[i-2] == ' ': ## no time here cause it would interfere and the milisecond difference will be fine
                self.r_old = self.r
                self.r = int((string[i+1:i+9].split('\\'))[0])
            
            if string[i] == 't' and string[i-1] == 't' and string[i-2] == 'a':
                try:
                    self.batt = float((string[i+2:i+9].split(' '))[0])
                except ValueError:
                    self.batt = 0.0

    
            i += 1
        
        if self.EstopCondition():
            self.Estop()

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
            angle += 35

        if keyboard.is_pressed('down') or keyboard.is_pressed('s'):
            speed -= 15

        if keyboard.is_pressed('right') or keyboard.is_pressed('d'):
            angle -= 35

        if keyboard.is_pressed('q'):
            self.startBeacon()

        if keyboard.is_pressed('e'):
            self.stopBeacon()


        return speed, angle

    def initJoystick(self):
        # Run the binnary as a separate process that will read the joysticks
        self.proc = subprocess.Popen("../../utilities/bin/joystick", stdout=subprocess.PIPE)
        # os.set_blocking(self.proc.stdout.fileno(), False)
        self.q = collections.deque(maxlen=1)
        t = threading.Thread(target=read_output, args=(self.proc, self.q.append))
        t.daemon = True
        t.start()
        
    def updateDirectionStick(self):
        # Read from the stdout of the binary and update the joysticks
        # tmp = self.proc.stdout.readline()
        try:
            tmp = self.q[0]
        except IndexError:
            tmp = 0

        if len(str(tmp)) < 8:
            speed = 0
            angle = 0

        else:
            angle = int(str(tmp)[2:5])
            speed = int(str(tmp)[-6:-3])
    
        return speed, angle

    def EstopCondition(self): ## Should ESTOP be initiated automatically // TODO
        derR,derL = self.DistanceDerivative()
        if derR  == 0:
            derR = 1e-33
        elif abs(derR) > 20:
            derR = 1e-33
        
        if derL == 0:  
            derL = 1e-33
        elif abs(derL) > 20:
            derL = 1e-33
        TimeToImpact = -min(self.l/derL, self.r/derR) 
        if 0 < TimeToImpact < 3:
            return True
        else:
            return False

    def DistanceDerivative(self):
        timediff = self.time_new - self.time_old
        if timediff == 0:
            timediff = 1e-33
        derL = (self.l - self.l_old) / timediff
        derR = (self.r - self.r_old) /  timediff
        return derL, derR
    

    def Estop(self):
        speed = -self.speed + 300
        self.set_speed(speed)
        time.sleep(1)
        self.stop()
        self.EstopF = True


def read_output(process, append):
    for line in iter(process.stdout.readline, ""):
        append(line)
