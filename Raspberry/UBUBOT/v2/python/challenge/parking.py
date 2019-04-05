#!/usr/bin/python3
from ububot.Initializer import UBUBOT
from ububot.Sensor.IR import SensorEvent
from ububot.Motor.MotorPair import MotorIdentifier
from time import sleep


if __name__ == '__main__':
    with UBUBOT(motors=True, sensors=True, motors_socket=True, serial_socket_capture=True, status_socket=True) as ububot:
        input("Press Enter to continue...")
        ububot.motors.advance_cm(110, speed=100)
        ububot.sensors.get_north().wait(SensorEvent.DETECT_START, timeout=4)
        ububot.motors.stop()
        ububot.motors.advance_cm(-40, speed=100)
        sleep(3)
        ububot.motors.move_by(MotorIdentifier.LEFT, speed=100, angle=-400)
        ububot.motors.move_by(MotorIdentifier.RIGHT, speed=80, angle=-400)
        ububot.sensors.get_south().wait(SensorEvent.DETECT_START, timeout=3)
        ububot.motors.stop()
        input("Press Enter to finish...")