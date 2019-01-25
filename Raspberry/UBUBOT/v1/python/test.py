#!/usr/bin/python3
from time import sleep

import lib.RPi.GPIO as GPIO
import lib.PCA9685 as DRIVER
from Motor.Motor import Motor
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
    motors['LB'] = Motor(driver, config.MotorDriverLeftPWM, config.MotorDriverLeftForwards,
                         config.MotorDriverLeftBackwards, factor=config.MotorLeftRatio)
    motors['RB'] = Motor(driver, config.MotorDriverRightPWM, config.MotorDriverRightForwards,
                         config.MotorDriverRightBackwards, factor=config.MotorRightRatio)
    for i in range(parser.parse_args().N):
        motors['LB'].update(4095)
        motors['RB'].update(-4095)
        sleep(1)
        motors['LB'].update(-4095)
        motors['RB'].update(4095)
        sleep(1)
        motors['LB'].update(4095)
        motors['RB'].update(4095)
        sleep(1)
        motors['LB'].update(-4095)
        motors['RB'].update(-4095)
        sleep(1)
    motors['LB'].update(0)
    motors['RB'].update(0)
