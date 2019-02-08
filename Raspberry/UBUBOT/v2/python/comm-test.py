#!/usr/bin/python3
import os, sys
import serial
import time

ser = serial.Serial('/dev/ttyUSB0',38400, timeout = 5)

forw = True
# listen for the input, exit if nothing received in timeout period
while True:
    print("...")
    if forw:
        ser.write(b'{{MOVT;B;180;250}}')
        print('FORWARDS')
    else:
        ser.write(b'{{MOVT;B;20;250}}')
        print('BACKWARDS')
    forw = not forw
    time.sleep(2)