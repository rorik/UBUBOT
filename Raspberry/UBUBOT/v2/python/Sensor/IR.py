#!/usr/bin/python3
import RPi.GPIO as GPIO
from enum import Enum


class SensorEvent(Enum):
    DETECT_START = GPIO.RISING
    DETECT_END = GPIO.FALLING


class IRSensor(object):
    _initialized_GPIO = False
    _event = None

    def __init__(self, pin):
        if not IRSensor._initialized_GPIO:
            GPIO.setmode(GPIO.BOARD)
            IRSensor._initialized_GPIO = True
        self._pin = pin

    def wait(self, event, timeout=2000):
        return GPIO.wait_for_edge(self._pin, event.value, timeout=timeout) is not None

    def add_callback(self, event, callback):
        if event != self._event:
            self._event == event
            GPIO.add_event_detect(self._pin, event.value)
        GPIO.add_event_callback(self._pin, callback)

    def reset(self):
        GPIO.remove_event_detect(self._pin)
