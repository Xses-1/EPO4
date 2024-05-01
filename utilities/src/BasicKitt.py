#!/bin/python3.10
import serial
import time
import os
import sys

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'inc'))
from KITT import KITT
        
if __name__ == '__main__':
<<<<<<< HEAD
    #kitt = KITT('COM10')
    kitt = KITT('/dev/rfcomm0')
=======
    kitt = KITT('COM10')
>>>>>>> 0aed99a04b6c30ae8805b62944dc8646b72565a4
    while(1):
        kitt.print_status()
        kitt.log_status()
        time.sleep(1)
        os.system('clear')


    kitt.serial.close()
