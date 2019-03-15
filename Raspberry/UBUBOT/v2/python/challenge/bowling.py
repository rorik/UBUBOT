#!/usr/bin/python3
from util.Initializer import UBUBOT
from Motor.MotorPair import MotorIdentifier, MotorPairDirection
from time import sleep


if __name__ == '__main__':
    with UBUBOT(motors=True, relays=True) as ububot:
        ububot.motors.advance_cm(10, speed=100)
        sleep(2)
        ububot.motors.turn_sharp(MotorPairDirection.SHARP_LEFT, speed=100, angle=90*2.4)
        sleep(2)
        ububot.motors.advance_cm(30, speed=100)
        sleep(3)
        ububot.motors.turn_sharp(MotorPairDirection.SHARP_RIGHT, speed=100, angle=90*2.4)
        sleep(2)
        ububot.relays.get_motor_1().off()
        sleep(1)
        ububot.relays.get_motor_1().on()
