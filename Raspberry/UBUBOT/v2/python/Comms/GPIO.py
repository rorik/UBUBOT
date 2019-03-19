#!/usr/bin/python3
import RPi.GPIO as GPIO


class GPIOObject(object):
    _initialized_GPIO = False

    def __init__(self, pin, name=None):
        GPIOObject.initialize_GPIO()
        self._pin = pin
        self.set_name(pin if name is None else name)
    
    def set_name(self, name):
        self._name = str(name)

    def get_name(self):
        return self._name

    def get_state(self):
        return GPIO.input(self._pin)

    @staticmethod
    def initialize_GPIO():
        if not GPIOObject._initialized_GPIO:
            GPIO.setmode(GPIO.BOARD)
            GPIOObject._initialized_GPIO = True

    @staticmethod
    def clean_up():
        GPIO.cleanup()
