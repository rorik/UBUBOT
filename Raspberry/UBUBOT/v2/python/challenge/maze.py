#!/usr/bin/python3
from ububot.Initializer import UBUBOT
from ububot.Motor.MotorPair import MotorIdentifier, MotorPairDirection
from time import sleep


if __name__ == '__main__':
    with UBUBOT(motors=True) as ububot:
        sleep(1)
        ububot.motors.move_by(MotorIdentifier.BOTH, 60, 500)
        sleep(3)
        ububot.motors.turn_sharp(MotorPairDirection.SHARP_RIGHT, speed=60, angle=90 * 2.3)
        sleep(3)
        ububot.motors.move_by(MotorIdentifier.BOTH, 60, 200)
        sleep(3)
        ububot.motors.turn_sharp(MotorPairDirection.SHARP_RIGHT, speed=60, angle=35 * 2.3)
        sleep(3)
        ububot.motors.move_by(MotorIdentifier.BOTH, 60, 500)
        sleep(3)
        ububot.motors.turn_sharp(MotorPairDirection.SHARP_RIGHT, speed=60, angle=40 * 2.3)
        sleep(3)
        ububot.motors.move_by(MotorIdentifier.BOTH, 60, 720)
        sleep(3)
        ububot.motors.turn_sharp(MotorPairDirection.SHARP_LEFT, speed=60, angle=90 * 2.3)
        sleep(3)
        ububot.motors.move_by(MotorIdentifier.BOTH, 60, 600)
        sleep(3)
        ububot.motors.stop()
