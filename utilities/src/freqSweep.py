#!/bin/python3.10
import serial
import time
import os
import sys

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'inc'))
from KITT import KITT
        
if __name__ == '__main__':
    kitt = KITT('COM13')
    #kitt = KITT('/dev/rfcomm0')
    while(1):
        for i in range(500,20000)[::100]:
            time.sleep(0.5)
            print(i)
            kitt.setBeacon(carrier_freq = i, bit_frequency = 50, repition_count = 2500, code = 0xB00B1E50)
            time.sleep(0.5)
            kitt.startBeacon()
            time.sleep(1)
            kitt.print_status()
            time.sleep(0.5)
            kitt.stopBeacon()
            time.sleep(0.5)
            kitt.print_status()

        break

    # std is 5000 hz

    kitt.serial.close()
    sys.exit(1)