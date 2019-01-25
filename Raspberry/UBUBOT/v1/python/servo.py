#!/usr/bin/python3
from time import sleep

import lib.RPi.GPIO as GPIO
import lib.PCA9685 as DRIVER
from Motor.Servo import Servo
from util.ConfigHelper import ConfigHelper
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('N', type=int, default=4)
    motors = {}
    config = ConfigHelper.load_config("/etc/cb/UBUBOT/config")
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    driver = DRIVER.PWM(bus_number=config.I2CBus)
    driver.frequency = config.MotorDriverFrequency
    servo = Servo(driver, 11, factor=1)
    for i in range(parser.parse_args().N):
        for i in range(60, 61):
            print(i*10)
            servo.update(i*10)
            sleep(1)
    servo.update(0)
