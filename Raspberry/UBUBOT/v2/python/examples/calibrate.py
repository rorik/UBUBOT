#!/usr/bin/python3
from ububot.Motor.MotorPair import MotorPairDirection
from ububot.Initializer import UBUBOT
from argparse import ArgumentParser
from sys import stdin, stdout
from tty import setraw
from termios import tcgetattr, tcsetattr, TCSADRAIN


def getChar():
    fd = stdin.fileno()
    old_settings = tcgetattr(fd)
    try:
        setraw(stdin.fileno())
        ch = stdin.read(1)
    finally:
        tcsetattr(fd, TCSADRAIN, old_settings)
    return ch


def sharp(ububot, speeds, angle):
    print("--- Calibrating sharp turn ({}°) ---".format(angle))
    print("Place the device in the target surface, make sure there's enough space.")
    print("Controls:")
    print("  - Up arrow/'A': Increase turn ratio.")
    print("  - Down arrow/'B': Decrease turn ratio.")
    print("  - Right arrow/'C': Increase ratio gain.")
    print("  - Left arrow/'D': Decrease ratio gain.")
    print("  - Space: Try again.")
    print("  - Enter: The device has turned", angle, "degrees.")
    direction = 0
    result = []

    gain = 0.1
    for speed in speeds:
        ratio = 2.0
        print("> SPEED [ {} ] <".format(str(speed).rjust(3)))
        print("Ratio = {:.3f}".format(ratio))
        key = getChar()
        while not (key == '\r' or key == '\n'):
            if key == 'A':
                ratio += gain
            elif key == 'B':
                ratio = max(0.1, ratio - gain)
            elif key == 'C':
                gain += 0.1
            elif key == 'D':
                gain = max(0, gain - 0.1)
            elif key == ' ':
                ububot.motors.turn_sharp(MotorPairDirection(direction), speed, angle * ratio)
                direction = (direction + 1) % len(MotorPairDirection)
            elif key == 'c':
                return None
            stdout.write("\033[F\033[K")
            print("Ratio = {:.3f}".format(ratio))
            key = getChar()
        result.append(ratio)
    return result


def advance(ububot, speeds, distance):
    print("--- Calibrating distance ({} cm) ---".format(distance))
    print("Place the device in the target surface, make sure there's enough space.")
    print("Controls:")
    print("  - Up arrow/'A': Increase distance ratio.")
    print("  - Down arrow/'B': Decrease distance ratio.")
    print("  - Right arrow/'C': Increase ratio gain.")
    print("  - Left arrow/'D': Decrease ratio gain.")
    print("  - Space: Try again.")
    print("  - Enter: The device has advanced", distance, "cm.")
    direction = 1
    result = []

    gain = 0.05
    for speed in speeds:
        ratio = 1.0
        print("> SPEED [ {} ] <".format(str(speed).rjust(3)))
        print("Ratio = {:.3f}".format(ratio))
        key = getChar()
        while not (key == '\r' or key == '\n'):
            if key == 'A':
                ratio += gain
            elif key == 'B':
                ratio = max(0.1, ratio - gain)
            elif key == 'C':
                gain += 0.1
            elif key == 'D':
                gain = max(0, gain - 0.1)
            elif key == ' ':
                ububot.motors.advance_cm(distance * ratio * direction, speed=speed)
                direction *= -1
            elif key == 'c':
                return None
            stdout.write("\033[F\033[K")
            print("Ratio = {:.3f}".format(ratio))
            key = getChar()
        result.append(ratio)
    return result


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('-t', '--turn-speed', type=int, nargs='+')
    parser.add_argument('-n', '--angle', type=int, default=90)
    parser.add_argument('-a', '--advance-speed', type=int, nargs='+')
    parser.add_argument('-d', '--distance', type=int, default=10)
    parser.add_argument('-sio', '--socket', dest='socket', action='store_const', const=True, default=False)
    args = parser.parse_args()

    if args.turn_speed is not None:
        t_speeds = []
        for speed in args.turn_speed:
            if speed not in t_speeds and speed > 0:
                t_speeds.append(speed)
        if len(t_speeds) == 0:
            raise ValueError('Expected at least one non-zero positive integer')
    else:
        t_speeds = [50, 100, 150, 200]

    if args.advance_speed is not None:
        a_speeds = []
        for speed in args.advance_speed:
            if speed not in a_speeds and speed > 0:
                a_speeds.append(speed)
        if len(a_speeds) == 0:
            raise ValueError('Expected at least one non-zero positive integer')
    else:
        a_speeds = [50, 100, 150, 200]

    print("Starting calibration.")
    print("Press 'c' at any moment to cancel the calibration process.")
    with UBUBOT(motors=True, serial_socket_capture=args.socket, motors_socket=args.socket) as ububot:
        t_ratios = sharp(ububot, t_speeds, args.angle)
        if t_ratios is None:
            exit(-1)
        a_ratios = advance(ububot, a_speeds, args.distance)
        print()
        print('Turn ratios:')
        for speed, ratio in zip(t_speeds, t_ratios):
            print("SPEED [ {} ] : {:.3f}".format(str(speed).rjust(3), ratio))
        if a_ratios is None:
            exit(-1)
        print('Distance ratios:')
        for speed, ratio in zip(a_speeds, a_ratios):
            print("SPEED [ {} ] : {:.3f}".format(str(speed).rjust(3), ratio))
        print()
