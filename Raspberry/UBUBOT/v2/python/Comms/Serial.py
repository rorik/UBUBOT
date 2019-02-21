#!/usr/bin/python3
import serial

class SerialCommunication:
    _connection = None

    def __init__(self):
        if SerialCommunication._connection is None:
            SerialCommunication._connection = serial.Serial(
                port='/dev/serial0',
                baudrate=230400,
                timeout=3,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS
                )

    def send(self, message, checksum=True, preview=False):
        data = "{{" + message
        if checksum:
            data += "$" + str(sum([ord(char) for char in message])%10)
        data += "}}"

        if preview:
            print(data)
        
        SerialCommunication._connection.write(data.encode('ascii'))
