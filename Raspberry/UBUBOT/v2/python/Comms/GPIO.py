#!/usr/bin/python3
import RPi.GPIO as GPIO


class GPIOObject(object):
    _initialized_GPIO = False

    def __init__(self, pin):
        GPIOObject.initialize_GPIO()
        self._pin = pin

    @staticmethod
    def initialize_GPIO():
        if not GPIOObject._initialized_GPIO:
            GPIO.setmode(GPIO.BOARD)
            GPIOObject._initialized_GPIO = True

    @staticmethod
    def clean_up():
        GPIO.cleanup()
