#!/usr/bin/python3
from ububot.Initializer import UBUBOT
from ububot.Sensor.IR import SensorEvent
from ububot.Motor.MotorPair import MotorIdentifier, MotorPairDirection
from ububot.Sound.Player import Player, Sounds
from time import sleep
from argparse import ArgumentParser

if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('mode', nargs='?', type=int, default=1)
    mode = parser.parse_args().mode
    with UBUBOT(motors=True, sensors=True, motors_socket=True, serial_socket_capture=True, status_socket=True) as ububot, Player() as player:
        if mode == 1:
            ububot.motors.turn_sharp(MotorPairDirection.SHARP_LEFT, 200, 180 * 4)
            sleep(1.2)
            ububot.motors.advance_cm(60, speed=200)
            sleep(1.2)
            ububot.motors.run(MotorIdentifier.LEFT, -200)
            ububot.motors.run(MotorIdentifier.RIGHT, 200)
            input("Press Enter to finish...")
        if mode == 2:
            ububot.motors.run(MotorIdentifier.LEFT, -120)
            ububot.motors.run(MotorIdentifier.RIGHT, -200)
            sleep(1.2)
            ububot.motors.run(MotorIdentifier.LEFT, 200)
            ububot.motors.run(MotorIdentifier.RIGHT, 130)
            sleep(1)
            print("Press Ctrl+C to finish...")
            try:
                while True:
                    ububot.motors.advance_cm(-20, speed=200)
                    sleep(0.8)
                    ububot.motors.advance_cm(20, speed=200)
                    sleep(0.8)
            except KeyboardInterrupt:
                pass
        if mode == 3:
            ububot.motors.run(MotorIdentifier.RIGHT, -120)
            ububot.motors.run(MotorIdentifier.LEFT, -200)
            sleep(1.2)
            ububot.motors.run(MotorIdentifier.RIGHT, 200)
            ububot.motors.run(MotorIdentifier.LEFT, 130)
            sleep(1)
            print("Press Ctrl+C to finish...")
            try:
                while True:
                    ububot.motors.advance_cm(-20, speed=200)
                    sleep(0.8)
                    ububot.motors.advance_cm(20, speed=200)
                    sleep(0.8)
            except KeyboardInterrupt:
                pass
        ububot.motors.stop() 