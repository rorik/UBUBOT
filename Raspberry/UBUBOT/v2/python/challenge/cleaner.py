#!/usr/bin/python3
from ububot.Initializer import UBUBOT
from ububot.Motor.MotorPair import MotorIdentifier, MotorPairDirection
from time import sleep


if __name__ == '__main__':
    with UBUBOT(motors=True, servos=True) as ububot:
        ububot.servos.get(7).angle(45)
        sleep(1)
        ububot.motors.turn_sharp(MotorPairDirection.SHARP_LEFT, speed=60, angle=45 * 2.2)
        sleep(2)
        ububot.motors.advance_cm(50, speed=60)
        sleep(2)
        ububot.motors.turn_sharp(MotorPairDirection.SHARP_RIGHT, speed=60, angle=45 * 2.2)
        sleep(2)
        ububot.motors.advance_cm(70, speed=60)
        sleep(4)
        ububot.motors.advance_cm(70, speed=60)
        sleep(4)
        ububot.motors.turn_sharp(MotorPairDirection.SHARP_RIGHT, speed=60, angle=45 * 2.2)
        sleep(2)
        ububot.motors.advance_cm(20, speed=60)
        sleep(3)
        ububot.motors.turn_sharp(MotorPairDirection.SHARP_LEFT, speed=60, angle=75 * 2.2)
        sleep(3)
        ububot.motors.advance_cm(35, speed=60)
        sleep(2)
        ububot.servos.get(7).angle(70)
        ububot.motors.stop()
