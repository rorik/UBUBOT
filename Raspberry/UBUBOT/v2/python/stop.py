#!/usr/bin/python3
from Comms.Serial import SerialCommunication

if __name__ == '__main__':
    com = SerialCommunication()
    com.send("STOP")
