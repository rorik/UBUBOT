#!/usr/bin/python3
from ububot.Motor.Servo import Servo, ChannelOutOfBoundsError
from ububot.Initializer import UBUBOT
from argparse import ArgumentParser
from time import sleep
from sys import stdout

if __name__ == '__main__':

    parser = ArgumentParser(description=__doc__)
    parser.add_argument('-c', '--channel', type=int, default=7)
    parser.add_argument('-a', '--angle', type=float, nargs='+', default=[0, 60, 120])
    parser.add_argument('-sio', '--socket', dest='socket', action='store_const', const=True, default=False)
    parser.add_argument('N', nargs='?', type=int, default=4)
    args = parser.parse_args()

    if not 0 <= args.channel <= 15:
        raise ChannelOutOfBoundsError("Channel = " + str(args.channel) + ". Range = [0, 15]")

    with UBUBOT(servos=True, status_socket=args.socket) as ububot:
        for i in range(args.N):
            for angle in args.angle:
                ububot.servos.get(args.channel).angle(angle)
                print("{}°".format(angle))
                sleep(1)
                stdout.write("\033[F\033[K")
