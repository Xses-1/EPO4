#!/bin/python3.10
import serial
import time
import os
import sys

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'inc'))
from KITT import KITT

if os.name == 'nt':
    comPort = 'COM13'
else:
    comPort = '/dev/rfcomm0'
        
if __name__ == '__main__':
    kitt = KITT(comPort)

    while(1):
        for i in range(1000,20000)[::1000]:
            time.sleep(0.5)
            print(i)
            kitt.setFreq(i)
            time.sleep(1)
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