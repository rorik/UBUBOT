#!/usr/bin/python3
import RPi.GPIO as GPIO
from Comms.GPIO import GPIOObject
from enum import Enum


class SensorEvent(Enum):
    DETECT_START = GPIO.RISING
    DETECT_END = GPIO.FALLING
    DETECT_ANY = GPIO.BOTH


class IRSensor(GPIOObject):
    _event = None

    def __init__(self, pin):
        GPIOObject.__init__(self, pin)
        GPIO.setup(self._pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def wait(self, event, timeout=2000):
        return GPIO.wait_for_edge(self._pin, event.value, timeout=timeout) is not None

    def add_callback(self, event, callback):
        if event != self._event:
            self._event == event
            GPIO.add_event_detect(self._pin, event.value)
        GPIO.add_event_callback(self._pin, callback)

    def reset(self):
        GPIO.remove_event_detect(self._pin)
