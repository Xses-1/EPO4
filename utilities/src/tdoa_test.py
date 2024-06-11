import sys
import os
import numpy as np
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'inc'))
from wavaudioread import wavaudioread
from var_ref_tdoa import TDOA

if __name__ == '__main__':
    T = TDOA()

    


    #y = T.tdoa_input(samples[0], samples[1], samples[2], samples[3], samples[4])

    Fs = 44100
    root_folder = Path("IntegrationTest.py").resolve().parent

    # y1 = wavaudioread(root_folder / "utilities/data/beacontestx250y250mic1.wav", Fs)
    # y2 = wavaudioread(root_folder / "utilities/data/beacontestx250y250mic2.wav", Fs)
    # y3 = wavaudioread(root_folder / "utilities/data/beacontestx250y250mic3.wav", Fs)
    # y4 = wavaudioread(root_folder / "utilities/data/beacontestx250y250mic4.wav", Fs)
    # y5 = wavaudioread(root_folder / "utilities/data/beacontestx250y250mic5.wav", Fs)

    # y = np.column_stack((y1,y2,y3,y4,y5))

    y = wavaudioread(root_folder / "utilities/data/record_x143_y296.wav", Fs)

    x = wavaudioread(root_folder / "utilities/data/reference.wav", Fs)    #Using reference recordings from all microphones
    
    x1 = x[:,0]
    x2 = x[:,0]
    x3 = x[:,0]
    x4 = x[:,0]
    x5 = x[:,0]

    #x = x[:,0]

    print(x1)

    c = T.localization(x1,x2,x3,x4,x5, y, Fs)
    print(c)

    error = np.sqrt((1.43-c[0])**2+(2.96-c[1])**2)

    print(error)
