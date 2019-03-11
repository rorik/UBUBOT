#!/usr/bin/python3
from Motor.MotorPair import MotorPair, MotorPairDirection, MotorIdentifier
from util.Initializer import UBUBOT
from argparse import ArgumentParser
from sys import stdin, stdout
import tty
import termios


def getChar():
    fd = stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(stdin.fileno())
        ch = stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def main(speed):
    print("Press enter or 'p' to exit")
    print("Direction = STOP")
    key = getChar()
    while not (key == '\r' or key == '\n' or key == 'p'):
        if key == 'w':
            ububot.motors.run(MotorIdentifier.BOTH, speed)
            direction = "Forwards"
        elif key == 's':
            ububot.motors.run(MotorIdentifier.BOTH, -speed)
            direction = "Backwards"
        elif key == 'a':
            ububot.motors.turn_sharp(MotorPairDirection.SHARP_LEFT, speed, 90)
            direction = "Sharp Left"
        elif key == 'd':
            ububot.motors.turn_sharp(MotorPairDirection.SHARP_RIGHT, speed, 90)
            direction = "Sharp Right"
        elif key == 'q':
            ububot.motors.move_by(MotorIdentifier.LEFT, speed=speed, angle=360)
            direction = "Left"
        elif key == 'e':
            ububot.motors.move_by(MotorIdentifier.RIGHT, speed=speed, angle=360)
            direction = "Right"
        elif key == 'z':
            ububot.motors.move_by(MotorIdentifier.LEFT, speed=speed, angle=-360)
            direction = "Reverse Left"
        elif key == 'e':
            ububot.motors.move_by(MotorIdentifier.RIGHT, speed=speed, angle=-360)
            direction = "Reverse Right"
        else:
            ububot.motors.stop()
            direction = "STOP"
        stdout.write("\033[F\033[K")
        print("Direction =", direction)
        key = getChar()
    ububot.motors.stop()

if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('-s', '--speed', type=int, default=200)
    parser.add_argument('-sio', '--socket', dest='socket', action='store_const', const=True, default=False)
    args = parser.parse_args()

    ububot = None
    try:
        ububot = UBUBOT(motors=True, serial_socket_capture=args.socket, motors_socket=args.socket)
        main(args.speed)
    finally:
        if ububot is not None:
            ububot.finalize()
