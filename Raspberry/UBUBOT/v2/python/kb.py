#!/usr/bin/python3
import curses
import os

from Motor.MotorPair import MotorPair, MotorPairDirection, MotorIdentifier


def main(win):
    speed=200
    win.nodelay(True)
    win.addstr("Direction = STOP")
    while True:
        try:
            key = win.getkey()
            if key == os.linesep:
                break
            elif key == 'w':
                motors.run(MotorIdentifier.BOTH, speed)
                direction = "Forwards"
            elif key == 's':
                motors.run(MotorIdentifier.BOTH, -speed)
                direction = "Backwards"
            elif key == 'a':
                motors.turn_sharp(MotorPairDirection.SHARP_LEFT, speed, 90)
                direction = "Sharp Left"
            elif key == 'd':
                motors.turn_sharp(MotorPairDirection.SHARP_RIGHT, speed, 90)
                direction = "Sharp Right"
            elif key == 'o':
                motors.run(MotorIdentifier.RIGHT, speed)
                direction = "Only Right Motor"
            elif key == 'p':
                motors.run(MotorIdentifier.LEFT, speed)
                direction = "Only Left Motor"
            else:
                motors.stop()
                direction = "STOP"
            win.clear()
            win.addstr("Direction = ")
            win.addstr(direction)
        except curses.error:
            pass
    motors.stop()


if __name__ == '__main__':
    motors = MotorPair()
    curses.wrapper(main)
