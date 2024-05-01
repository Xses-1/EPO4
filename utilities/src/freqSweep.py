#!/bin/python3.10
import serial
import time
import os
import sys

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'inc'))
from KITT import KITT
from Audio import Audio
        
if __name__ == '__main__':
    #kitt = KITT('COM10')
    kitt = KITT('/dev/rfcomm0')
    while(1):
        for i in range(500,20000)[::100]:
            kitt.setBeacon(carrier_freq = i, bit_frequency = 50, repition_count = 2500, code = 0xB00B1E50)
            kitt.startBeacon()
            time.sleep(0.5)
            kitt.stopBeacon()

        break


            
            


    kitt.serial.close()
    sys.exit(1)