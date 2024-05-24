#!/bin/python3.10
import serial
import time
import os

class KITT:
    def __init__(self, port, baudrate=115200):
        self.serial = serial.Serial(port, baudrate, rtscts=True)

    def sitrep(self):
        self.serial.write(b'Sd\n')
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

if __name__ == '__main__':
    kitt = KITT('/dev/rfcomm0')
    while(1):
        kitt.print_status()
        time.sleep(0.008)
        os.system('clear')
