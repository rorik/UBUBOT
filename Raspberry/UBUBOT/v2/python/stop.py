#!/usr/bin/python3
from Comms.Serial import SerialCommunication

if __name__ == '__main__':
    try:
        SerialCommunication().send("STOP")
    finally:
        SerialCommunication.disconnect()
