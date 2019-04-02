#!/usr/bin/python3
from ububot.Motor.MotorPair import MotorPair, MotorPairDirection, MotorIdentifier
from ububot.Initializer import UBUBOT
from ububot.Sound.Player import Player, Sounds
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

def main(ububot, speed, player):
    print("Press enter or 'p' to exit")
    print("Direction = STOP")
    key = getChar()
    relays = [True] * 4
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
        elif key == '1':
            relays[0] = not relays[0]
            ububot.relays.get_motor_1().set_state(relays[0])
            direction = "Relay 1"
        elif key == '2':
            relays[1] = not relays[1]
            ububot.relays.get_motor_2().set_state(relays[1])
            direction = "Relay 2"
        elif key == '3':
            relays[2] = not relays[2]
            ububot.relays.get_light().set_state(relays[2])
            direction = "Relay 3"
        elif key == '4':
            relays[3] = not relays[3]
            ububot.relays.get_buzzer().set_state(relays[3])
            direction = "Relay 4"
        elif key == '5':
            sound = player.play_random()
            direction = "Playing " + sound.name
        elif key == '6':
            player.stop()
            direction = "Stopping sound"
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

    with UBUBOT(motors=True, relays=True, serial_socket_capture=args.socket, motors_socket=args.socket, status_socket=args.socket, sensors=args.socket) as ububot, Player() as player:
        main(ububot, args.speed, player)
