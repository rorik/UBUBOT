#!/usr/bin/python3
from time import sleep
from threading import Thread
from atexit import register
from serial import Serial, PARITY_NONE, STOPBITS_ONE, EIGHTBITS

class SerialCommunication:
    _connection = None

    def __init__(self, redundancy=2):
        self._redundancy = max(1, redundancy)
        if SerialCommunication._connection is None:
            SerialCommunication._connection = Serial(
                    port='/dev/serial0',
                    baudrate=230400,
                    timeout=0,
                    parity=PARITY_NONE,
                    stopbits=STOPBITS_ONE,
                    bytesize=EIGHTBITS
                )
            register(SerialCommunication.disconnect)

    def send(self, message, checksum=True, preview=False):
        data = "{{" + message
        if checksum:
            data += "$" + str(sum([ord(char) for char in message])%10)
        data += "}}"
        data = data.encode('ascii')

        if preview:
            print(data)
        
        for _ in range(self._redundancy):
            SerialCommunication._connection.write(data)

    def read_line(self):
        return SerialCommunication._connection.read_until()

    def flush_in(self):
        SerialCommunication._connection.reset_input_buffer()

    
    @staticmethod
    def disconnect():
        if SerialCommunication._connection is not None:
            SerialCommunication._connection.close()
            SerialCommunication._connection = None


class SerialCapture(SerialCommunication, Thread):

    def start(self, output=lambda read: print(read, end='')):
        Thread.__init__(self)
        self.running = True
        self.set_output(output)
        Thread.start(self)
    
    def run(self):
        line = ""
        while (self.running and SerialCommunication._connection and SerialCommunication._connection.is_open):
            while (SerialCommunication._connection.in_waiting > 0):
                read = self.read_line()
                try:
                    read = read.decode('ascii')
                    line += read
                    if line[-1] == '\n':
                        self.output(line)
                        line = ""
                except:
                    pass
            sleep(0.05)
    
    def stop(self):
        self.running = False
    
    def set_output(self, function):
        self.output = function