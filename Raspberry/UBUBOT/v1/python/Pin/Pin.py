#!/usr/bin/python3
from enum import Enum


class Pin(object):
    def __init__(self, number, name=None, pin_type=None, value=0):
        self.number = number
        self.name = name
        self.pin_type = pin_type
        self.value = value


class PinType(Enum):
    GPIO = 0
    V5 = 1
    V3 = 2
    GND = 3
    I2C = 4
