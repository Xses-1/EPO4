#!/bin/python3.10
import serial
import time
import os
import sys

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'inc'))
from KITT import KITT
        
if __name__ == '__main__':
    kitt = KITT('/dev/rfcomm0')
    while(1):
        kitt.print_status()
        time.sleep(1)
        os.system('clear')


    
    kitt.serial.close()
