#!/usr/bin/python3
import curses
import os

from Motor.MotorPair import MotorPair, MotorPairDirection
from Sensor.us_locker import USLocker
from util.ConfigHelper import ConfigHelper


def main(win):
    speed=4095
    win.nodelay(True)
    win.addstr("Direction = STOP")
    while 1:
        try:
            key = win.getkey()
            if key == os.linesep:
                break
            elif key == 'w':
                motors.move(MotorPairDirection.FORWARDS, speed=speed)
                direction = "Forwards"
            elif key == 's':
                motors.move(MotorPairDirection.BACKWARDS)
                direction = "Backwards"
            elif key == 'a':
                motors.move(MotorPairDirection.SHARP_LEFT)
                direction = "Sharp Left"
            elif key == 'd':
                motors.move(MotorPairDirection.SHARP_RIGHT)
                direction = "Sharp Right"
            elif key == 'q':
                motors.move(MotorPairDirection.POLAR, angle=45)
                direction = "Diagonal Left"
            elif key == 'e':
                motors.move(MotorPairDirection.POLAR, angle=-45)
                direction = "Diagonal Right"
            elif key == 'o':
                motors.move(MotorPairDirection.VECTOR, speed=0)
                direction = "Right Alone"
            elif key == 'p':
                motors.move(MotorPairDirection.VECTOR, speed_secondary=0)
                direction = "Left Alone"
            else:
                motors.move(MotorPairDirection.STOP)
                direction = "STOP"
            win.clear()
            win.addstr("Direction = ")
            win.addstr(direction)
        except curses.error:
            pass
    lock.stop()
    motors.move(MotorPairDirection.STOP)


if __name__ == '__main__':
    config = ConfigHelper.load_config("/etc/cb/UBUBOT/config")
    motors = MotorPair(config)
    lock = USLocker(config, motors)
    lock.start()
    curses.wrapper(main)
