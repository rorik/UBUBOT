#!/usr/bin/python3
import RPi.GPIO as GPIO
from Comms.GPIO import GPIOObject


class Relay(GPIOObject):

    def __init__(self, pin, initial_state=GPIO.HIGH, state_listener=None, name=None):
        GPIOObject.__init__(self, pin, name)
        GPIO.setup(self._pin, GPIO.OUT)
        self._state_listener = state_listener
        self.set_state(initial_state)

    def on(self):
        self.set_state(GPIO.HIGH)

    def off(self):
        self.set_state(GPIO.LOW)

    def set_state(self, state):
        GPIO.output(self._pin, state)
        if self._state_listener is not None:
            self._state_listener({"pin": self._pin, "state": state, "name": self.get_name(), "type": "Relay"})
