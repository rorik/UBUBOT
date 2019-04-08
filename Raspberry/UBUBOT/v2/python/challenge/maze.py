#!/usr/bin/python3
from ububot.Initializer import UBUBOT
from ububot.Motor.MotorPair import MotorIdentifier, MotorPairDirection
from time import sleep


if __name__ == '__main__':
    with UBUBOT(motors=True) as ububot:
        ububot.motors.advance_cm(30, speed=100)
        sleep(1)
        ububot.motors.turn_sharp(MotorPairDirection.SHARP_LEFT, speed=60, angle=90 * 2.3)
        sleep(3)
        ububot.motors.advance_cm(200, speed=100)
        sleep(3)
        ububot.motors.turn_sharp(MotorPairDirection.SHARP_RIGHT, speed=60, angle=90 * 2.3)
        sleep(3)
        ububot.motors.advance_cm(180, speed=100)
        sleep(3)
        ububot.motors.turn_sharp(MotorPairDirection.SHARP_RIGHT, speed=60, angle=90 * 2.3)
        sleep(3)
        ububot.motors.advance_cm(210, speed=100)
        sleep(3)
        ububot.motors.stop() 
