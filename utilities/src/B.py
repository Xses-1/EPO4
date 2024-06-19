from A_TDOA import Challenge_A
import numpy as np
import time
import tkinter as tk


def inputGUI():
    global tX1, tY1, tX2, tY2, cX, cY, Theta
    root = tk.Tk()
    root.geometry("600x400")
    root.title('KITT Input GUI')

    def Submit():
        global tX1, tY1, tX2, tY2, cX, cY, Theta
        cX =        float(carX.get())
        cY =        float(carY.get())
        Theta =     np.pi/2*float(carT.get())
        tX1 =       float(X1.get())
        tY1 =       float(Y1.get())
        tX2 =       float(X2.get())
        tY2 =       float(Y2.get())

        root.destroy()
        root.quit()

    X1 = tk.StringVar()
    Y1 = tk.StringVar()
    X2 = tk.StringVar()
    Y2 = tk.StringVar()
    carX = tk.StringVar()
    carY = tk.StringVar()
    carT = tk.StringVar()

    NameLabel = tk.Label(root, text = 'Please enter all relevant Values')
    CarLabel = tk.Label(root, text = 'Car Position [x, y, T]: ')
    Car1X = tk.Entry(root, textvariable= carX)
    Car1Y = tk.Entry(root, textvariable= carY)
    Car1T = tk.Entry(root, textvariable= carT)

    Target1Label = tk.Label(root, text = 'Target1 [x, y]: ')
    Target1X = tk.Entry(root, textvariable= X1)
    Target1Y = tk.Entry(root, textvariable= Y1)

    Target2Label = tk.Label(root, text = 'Target2 [x, y]: ')
    Target2X = tk.Entry(root, textvariable= X2)
    Target2Y = tk.Entry(root, textvariable= Y2)

    sub_btn=tk.Button(root,text = 'Submit', command = Submit)

    NameLabel       .grid(row = 0, column = 0)
    CarLabel        .grid(row = 1, column = 0)
    Car1X           .grid(row = 1, column = 1)
    Car1Y           .grid(row = 1, column = 2)
    Car1T           .grid(row = 1, column = 3)
    Target1Label    .grid(row = 2, column = 0)
    Target1X        .grid(row = 2, column = 1)
    Target1Y        .grid(row = 2, column = 2)
    Target2Label    .grid(row = 3, column = 0)
    Target2X        .grid(row = 3, column = 1)
    Target2Y        .grid(row = 3, column = 2)
    sub_btn         .grid(row = 4, column = 0)

    root.mainloop()


if __name__ == '__main__':
    # Define static variables
    target_offset = 0.3      # The distance from the tarrget to still count success
    calibration_delay = 15     # The amount of loop iterations before the TDOA calibration
    sleeptime = 0.1

    # Setup function:

    '''

    # Ask for the target input
    print("Give First target coordinates in meters separated by a new line")
    print("in following notation: \"X\\nY\", ex. \"0.69\\n4.20\"")
    tX1 = float(input())
    tY1 = float(input())

    print("Give Second target coordinates in meters separated by a new line")
    print("in following notation: \"X\\nY\", ex. \"0.69\\n4.20\"")
    tX2 = float(input())
    tY2 = float(input())

    # For testing the initail position can be typed in
    print("Type in the current position in meters and angle in Radians / (np.pi/2)")
    cX = float(input())
    cY = float(input())
    Theta = np.pi/2*float(input())
    '''

    tX1 = 0.0
    tY1 = 0.0
    tX2 = 0.0
    tY2 = 0.0
    cX = 0.0
    cY = 0.0
    Theta = 0.0

    inputGUI()

    print(tX1, tY1, tX2, tY2, cX, cY, Theta)
    ## Run challenge A for the First time
    cX, cY, Theta = Challenge_A(cX, cY, Theta, tX1, tY1, target_offset, calibration_delay, sleeptime)

    print(cX, cY, Theta)

    ## wait the measuring delay
    time.sleep(10)

    ## Run challenge A the second time
    cX, cY, Theta = Challenge_A(cX, cY, Theta, tX2, tY2, target_offset, calibration_delay, sleeptime)
