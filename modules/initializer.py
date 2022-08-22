import serial

class Initializer:
    def initializer(self):
        trm240 = serial.Serial(
            "/dev/ttyUSB2",
            115200,
            bytesize=8,
            parity='N',
            stopbits=1,
            timeout=1,
            rtscts=False,
            dsrdtr=False,
            write_timeout=1)
        return trm240