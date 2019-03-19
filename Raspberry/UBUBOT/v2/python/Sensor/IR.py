#!/usr/bin/python3
import RPi.GPIO as GPIO
from Comms.GPIO import GPIOObject
from enum import Enum


class SensorEvent(Enum):
    DETECT_START = GPIO.FALLING
    DETECT_END = GPIO.RISING
    DETECT_ANY = GPIO.BOTH


class IRSensor(GPIOObject):
    def __init__(self, pin, state_listener=None, name=None):
        GPIOObject.__init__(self, pin, name)
        GPIO.setup(self._pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self._state_listener = state_listener
        self._callbacks = {SensorEvent.DETECT_ANY: set(), SensorEvent.DETECT_START: set(), SensorEvent.DETECT_END: set()}
        GPIO.add_event_detect(self._pin, SensorEvent.DETECT_ANY.value, callback=self._send_callbacks)

    def _send_callbacks(self, *args):
        state = self.get_state()
        if self._state_listener is not None:
            self._state_listener({"pin": self._pin, "state": state, "name": self.get_name(), "type": "Sensor"})
        for callback in self._callbacks.get(SensorEvent.DETECT_ANY).union(self._callbacks.get(SensorEvent.DETECT_END if state else SensorEvent.DETECT_START)):
            callback(state)

    def wait(self, event, timeout=2000):
        return GPIO.wait_for_edge(self._pin, event.value, timeout=timeout) is not None

    def add_callback(self, event, callback):
        group = self._callbacks.get(event)
        if group is not None:
            group.add(callback)

    def remove_callback(self, event, callback):
        group = self._callbacks.get(event)
        if group is not None:
            group.remove(event)

    def reset(self):
        GPIO.remove_event_detect(self._pin)
