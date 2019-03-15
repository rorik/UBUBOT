#!/usr/bin/python3
from Relay.Relay import Relay
from util.Initializer import UBUBOT
from argparse import ArgumentParser
from time import sleep

if __name__ == '__main__':

    parser = ArgumentParser(description=__doc__)
    parser.add_argument('N', nargs='?', type=int, default=4)
    N = parser.parse_args().N

    with UBUBOT(relays=True) as ububot:
        for i in range(N):
            print("off")
            ububot.relays.off()
            sleep(1)
            print("on")
            ububot.relays.on()
            sleep(1)
