#!/bin/python3.10
import keyboard    
import sys    
import os    
import time    

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'inc'))    
from KITT import KITT


# Setup function:
# Ask for the target input
print("Give target coordinates separated by a new line - \"X\\nY\", ex. \"69\\n420\"")
tX = int(input())
tY = int(input())

# Checiking the os and connecting to the port
if os.name == 'nt':    
    comPort = 'COM22'    
else:    
    comPort = '/dev/rfcomm0'

kitt = KITT(comPort)






# The loop function:
while(1):
