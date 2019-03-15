#!/usr/bin/python3
from util.Initializer import UBUBOT
from Comms.Serial import SerialCommunication, SerialCapture
from Comms.Socket import SocketCommunication
import argparse
import time

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('N', type=int, default=4)

    forw = True
    with UBUBOT(serial_socket_capture=True) as ububot:
        for i in range(parser.parse_args().N * 2):
            if forw:
                ububot.serial.send("MOVB;B;180;50")
                print('FORWARDS')
            else:
                ububot.serial.send("MOVB;B;-180;50")
                print('BACKWARDS')
            forw = not forw
            time.sleep(1)
