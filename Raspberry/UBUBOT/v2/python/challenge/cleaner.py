#!/usr/bin/python3
from ububot.Initializer import UBUBOT
from ububot.Motor.MotorPair import MotorIdentifier, MotorPairDirection
from time import sleep


if __name__ == '__main__':
    with UBUBOT(motors=True, servos=True) as ububot:
        ububot.servos.get(7).angle(45)
        sleep(1)
        ububot.motors.move_by(MotorIdentifier.BOTH, 60, 360)
        sleep(1)
        ububot.motors.turn_sharp(MotorPairDirection.SHARP_RIGHT, speed=60, angle=70 * 2.7)
        sleep(1)
        ububot.motors.move_by(MotorIdentifier.BOTH, 60, 360)
        sleep(1)
        ububot.servos.get(7).angle(70)
        ububot.motors.move_by(MotorIdentifier.BOTH, 60, -300)
        sleep(1)
        ububot.motors.turn_sharp(MotorPairDirection.SHARP_RIGHT, speed=60, angle=270 * 2.7)
        sleep(3)
        ububot.servos.get(7).angle(45)
        sleep(1)
        ububot.motors.stop()
