#!/usr/bin/python3
from Motor.MotorPair import MotorPair, MotorPairDirection, MotorIdentifier
from Sensor.IR import SensorEvent
from util.Initializer import initialize
from argparse import ArgumentParser
from time import sleep

if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('N', type=int, default=4)
    
    motors, sensors = initialize()

    for i in range(parser.parse_args().N * 4):
        motors.run(MotorIdentifier.BOTH, speed=100)
        sensors.get_north().wait(SensorEvent.DETECT_START, timeout=1000)
        motors.advance_cm(-2, speed=50)
        motors.turn_sharp(MotorPairDirection.SHARP_RIGHT, speed=100, angle=90)
        sleep(1)


