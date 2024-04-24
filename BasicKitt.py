import serial

class KITT:
    def __init__(self, port, baudrate=115200):
        self.serial = serial.Serial(port, baudrate, rtscts=True)
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

    def sitrep(self):
        self.serial.write(b'S\n')
        status = self.serial.read_until(b'\x04')
        return status

    def __del__(self):
        self.serial.close()
     
        
if __name__ == '__main__':
    kitt = KITT('/dev/rfcomm0')
    string = str(kitt.sitrep())
    #print(string.split('\n'))
    
    i = 0;
    while i < len(string):
        if string[i] == "\\" and string [i+1] == "n":
            print()
            i = i + 1
            
        else:
            print(string[i], end='')

        i = i + 1

    
    kitt.serial.close()
