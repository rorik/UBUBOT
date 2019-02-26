#!/usr/bin/python3
from Comms.Serial import SerialCommunication
import argparse
import time

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('N', type=int, default=4)
    com = SerialCommunication()

    forw = True
    for i in range(parser.parse_args().N * 2):
        if forw:
            com.send("MOVB;B;180;50")
            print('FORWARDS')
        else:
            com.send("MOVB;B;-180;50")
            print('BACKWARDS')
        forw = not forw
        time.sleep(2)

    SerialCommunication.disconnect()