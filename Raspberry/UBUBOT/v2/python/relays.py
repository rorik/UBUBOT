#!/usr/bin/python3
from Relay.Relay import Relay
from util.Initializer import UBUBOT
from argparse import ArgumentParser
from time import sleep

if __name__ == '__main__':

    parser = ArgumentParser(description=__doc__)
    parser.add_argument('N', nargs='?', type=int, default=4)
    parser.add_argument('-sio', '--socket', dest='socket', action='store_const', const=True, default=False)
    args = parser.parse_args()

    with UBUBOT(relays=True, status_socket=args.socket) as ububot:
        for i in range(args.N):
            print("off")
            ububot.relays.off()
            sleep(1)
            print("on")
            ububot.relays.on()
            sleep(1)
