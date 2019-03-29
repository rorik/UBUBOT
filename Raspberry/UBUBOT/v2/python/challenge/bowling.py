#!/usr/bin/python3
from ububot.Initializer import UBUBOT
from ububot.Motor.MotorPair import MotorIdentifier, MotorPairDirection
from time import sleep


if __name__ == '__main__':
    with UBUBOT(motors=True, relays=True, motors_socket=True, serial_socket_capture=True, status_socket=True) as ububot:
        ububot.motors.advance_cm(61, speed=100)
        sleep(4)
        ububot.motors.turn_sharp(MotorPairDirection.SHARP_LEFT, speed=100, angle=90*2.5)
        sleep(2)
        ububot.motors.advance_cm(40, speed=100)
        sleep(3)
        ububot.relays.get_motor_1().off()
        sleep(1)
        ububot.relays.get_motor_1().on()
