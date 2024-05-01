import sys
import os

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'inc'))

from KITT import KITT


comport = 'COM10'
if __name__ == '__main__':
    kitt = KITT(comport)

    while True:
        
        kitt.log_status()