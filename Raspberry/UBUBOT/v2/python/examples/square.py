#!/usr/bin/python3
from ububot.Motor.MotorPair import MotorIdentifier, MotorPairDirection
from ububot.Sensor.IR import SensorEvent
from ububot.Initializer import UBUBOT
from argparse import ArgumentParser
from time import sleep

if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('N', nargs='?', type=int, default=2)

    ububot = None
    with UBUBOT(motors=True, sensors=True) as ububot:
        for i in range(parser.parse_args().N * 4):
            ububot.motors.run(MotorIdentifier.BOTH, speed=100)
            ububot.sensors.get_north().wait(SensorEvent.DETECT_START, timeout=1)
            ububot.motors.advance_cm(-5, speed=50)
            sleep(1)
            ububot.motors.turn_sharp(MotorPairDirection.SHARP_RIGHT, speed=100, angle=90)
            sleep(1)
