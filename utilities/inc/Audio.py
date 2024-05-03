import pyaudio
import numpy as np
from scipy.io.wavfile import write
import sys
'''
Class for interacting with the microphones and 
'''

class Audio:
    def __init__(self):
        self.handle = pyaudio.PyAudio()
        self.Fs = 44100
        index = self._detect_microphones()[0]
        self.microphones = self.handle.open(input_device_index= index,
                                            channels=5,
                                            format = pyaudio.paInt16,
                                            rate = self.Fs,
                                            input = True)
        self.playDevice = self.handle.open(format=pyaudio.paInt16, channels=1, rate=self.Fs, output=True)

    def _detect_microphones(self):
        j = []
        for i in range(self.handle.get_device_count()):
            devive_info = self.handle.get_device_info_by_index(i)
            if "AudioBox 1818" in devive_info['name'] and "Microfoon" in devive_info['name']:
                j.append(i)

        if len(j) == 0:
            print("AudioBox 1818 not found, please try again")
            sys.exit(-1)
        print(j)

        return j

    def sample(self, N):
        return np.frombuffer(self.microphones.read(N), dtype='int16')

    def split_data(self,data):
        mic1 = data[0::5]
        mic4 = data[1::5]
        mic2 = data[2::5]
        mic3 = data[3::5]
        mic5 = data[4::5]

        return [mic1,mic2,mic3,mic4,mic5]

    def play_sound(self, array):
        play = self.handle.open(format=pyaudio.paInt16, channels=1, rate=self.Fs, output=True)
        play.write(array.tobytes())
        play.stop_stream()
        play.close()

    def writeAlltoWave(self, mic1, mic2,mic3,mic4,mic5, fileappendix = ''):
        write(f'{fileappendix}mic1.wav', self.Fs, mic1.astype(np.int16))
        write(f'{fileappendix}mic2.wav', self.Fs, mic2.astype(np.int16))
        write(f'{fileappendix}mic3.wav', self.Fs, mic3.astype(np.int16))
        write(f'{fileappendix}mic4.wav', self.Fs, mic4.astype(np.int16))
        write(f'{fileappendix}mic5.wav', self.Fs, mic5.astype(np.int16))

    def write1toWav(self, data, filename = "File.wav"):
        write(filename, self.Fs, data)

    def writeto1Wav(self,  mic1, mic2,mic3,mic4,mic5, filename = "File.wav"):
        write(filename, self.Fs, [mic1.astype(np.int16),mic2.astype(np.int16),mic3.astype(np.int16),mic4.astype(np.int16),mic5.astype(np.int16)])
