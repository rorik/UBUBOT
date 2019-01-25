#!/usr/bin/python3
from enum import Enum

class MotorDirection(Enum):
    STOP = 0
    FORWARDS = 1
    BACKWARDS = 2
    ALL = 3


class Servo(object):
    direction = MotorDirection.STOP
    locked = MotorDirection.STOP

    def __init__(self, driver, channel, factor=1.0, speed=0, frequency=50,
                 reduction=0.0):
        if not -1.0 <= factor <= 1.0:
            raise FactorOutOfBoundsError("Factor = " + str(factor) + ". Range = [0, 1]")
        if not 0 <= reduction <= 1.0:
            raise FactorOutOfBoundsError("Reduction = " + str(factor) + ". Range = [0, 1]")
        if not 1 <= frequency <= 1000:
            raise FrequencyOutOfBoundsError("Frequency = " + str(frequency) + ". Range = [1, 1000]")
        self.factor = factor
        self.reduction = reduction
        self.speed = speed
        self.channel = channel
        self.driver = driver

    def toggle(self, direction):
        self.direction = direction
        self.driver.write(self.channel, 0, 4095 if direction == MotorDirection.FORWARDS else 0)

    def update(self, speed=None):
        if speed is not None:
            self.speed = speed
        if abs(self.speed) > 4095:
            raise SpeedOutOfBoundsError("Speed = " + str(self.speed) + ". MAXIMUM = +/- 4095")
        if self.speed == 0:
            if self.direction != MotorDirection.STOP:
                self.toggle(MotorDirection.STOP)
            return self.stop()
        elif self.speed > 0:
            if self.locked == MotorDirection.FORWARDS or self.locked == MotorDirection.ALL:
                return self.stop()
            if self.direction != MotorDirection.FORWARDS:
                self.toggle(MotorDirection.FORWARDS)
        else:
            if self.locked == MotorDirection.BACKWARDS or self.locked == MotorDirection.ALL:
                return self.stop()
            if self.direction != MotorDirection.BACKWARDS:
                self.toggle(MotorDirection.BACKWARDS)
        self.driver.write(self.channel, 0, abs(int(self.speed * self.factor * (1 - self.reduction))))

    def stop(self):
        self.driver.write(self.channel, 0, 0)


class MotorError(Exception):
    pass


class SpeedOutOfBoundsError(MotorError):
    def __init__(self, message="", expression=None):
        self.expression = expression
        self.message = message


class FactorOutOfBoundsError(MotorError):
    def __init__(self, message="", expression=None):
        self.expression = expression
        self.message = message


class FrequencyOutOfBoundsError(MotorError):
    def __init__(self, message="", expression=None):
        self.expression = expression
        self.message = message
