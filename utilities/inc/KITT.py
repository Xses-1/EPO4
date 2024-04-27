class KITT:
    def __init__(self, port, baudrate=115200):
        self.serial = None
        self.EstopF = False
        self.BeaconFlag = False
        for i in range(3):
            try:
                self.serial = serial.Serial(port, baudrate, rtscts=True)
            except serial.serialutil.SerialException:
                print(i)
        if self.serial == None:
            raise Exception
            
        # state variables such as speed, angle are defined here

    def send_command(self, command):
        self.serial.write(command.encode())

    def set_speed(self, speed):
        self.send_command(f'M{speed}\n')

    def set_angle(self, angle):
        self.send_command(f'D{angle}\n')

    def stop(self):
        self.set_speed(150)
        self.set_angle(150)

    def setBeacon(self, carrier_freq = 1000, bit_frequency = 5000, repition_count = 2500, code = 0xDEADBEEF):
        carrier_freq = carrier_freq.to_bytes(2, byteorder= 'big')
        self.serial.write( b'F' + carrier_freq + b'\n')
        bit_frequency = bit_frequency.to_bytes(2, byteorder= 'big')
        self.serial.write(b'B' + bit_frequency + b'\n')
        repition_count = repition_count.to_bytes(2, byteorder= 'big')
        self.serial.write(b'R' + repition_count + b'\n')
        code = code.to_bytes(4, byteorder= 'big')
        self.serial.write(b'C' + code + b'\n')

    def startBeacon(self):
        if self.BeaconFlag == True:
            return
        else:    
            self.serial.write(b'A1\n')
            self.BeaconFlag = True
    
    def stopBeacon(self):
        if self.BeaconFlag == True:
            self.serial.write(b'A0\n')
            self.BeaconFlag = False
        else:    
            return

    def sitrep(self):
        self.serial.write(b'S\n')
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
    
        # This routine splits the string and puts it
        # into variables that can be then logged
        i = 0
        while i < len(string):
            if string[i] == ':' and string[i-1] == 'n' and string[i-2] == 'o':

        

    def Estop(self):
        self.set_speed(135)
        time.sleep(0.5)
        self.stop()
        self.EstopF = True

    def __del__(self):
        self.serial.close()

