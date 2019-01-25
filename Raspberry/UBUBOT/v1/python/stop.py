#!/usr/bin/python3
import lib.RPi.GPIO as GPIO
import lib.PCA9685 as DRIVER
from Motor.Motor import Motor
from util.init import init_config

if __name__ == '__main__':
    motors = {}
    config = init_config("/etc/cb/UBUBOT/config")
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    driver = DRIVER.PWM(bus_number=config['BUS'])
    driver.frequency = config['MOT_DRF']
    motors['LB'] = Motor(driver, config['MOT_DRL'], config['MOT_LBF'], config['MOT_LBB'], factor=config['MOT_LBR'])
    motors['RB'] = Motor(driver, config['MOT_DRR'], config['MOT_RBF'], config['MOT_RBB'], factor=config['MOT_RBR'])
    motors['LB'].update(0)
    motors['RB'].update(0)
