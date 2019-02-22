#!/usr/bin/python3
import RPi.GPIO as GPIO
from Comms.GPIO import GPIOObject


class Relay(GPIOObject):

    def __init__(self, pin):
        GPIOObject.__init__(self, pin)
        GPIO.setup(self._pin, GPIO.OUT)

    def on(self):
        self.set_state(GPIO.HIGH)

    def off(self):
        self.set_state(GPIO.LOW)

    def get_state(self):
        return GPIO.input(self._pin)

    def set_state(self, state):
        GPIO.output(self._pin, state)
