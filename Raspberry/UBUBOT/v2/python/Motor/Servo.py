#!/usr/bin/python3
from enum import Enum
from util.PCA9685 import PWM as Driver
from Motor.MotorPair import MotorError

class Servo(object):
    _driver = None

    def __init__(self, channel, min_pwn=80, max_pwm=520, max_angle=120, state_listener=None):
        if not 0 <= channel <= 15:
            raise ChannelOutOfBoundsError("Channel = " + str(channel) + ". Range = [0, 15]")
        self._channel = channel
        self._pwm_ratio = (max_pwm - min_pwn) / max_angle
        self._pwm_offset = min_pwn
        self._pwm_limit = max_pwm
        self._state_listener = state_listener
        if Servo._driver is None:
            Servo._driver = Driver()
            Servo._driver.frequency = 50

    def angle(self, angle=0.0):
        self.update(self._pwm_ratio * angle + self._pwm_offset)
    
    def update(self, pwm):
        pwm = abs(int(pwm))
        if not 0 <= pwm <= 4095:
            raise ChannelOutOfBoundsError("PWM = " + str(pwm) + ". Range = [0, 4095]")
        Servo._driver.write(self._channel, 0, pwm)
        if self._state_listener is not None:
            self._state_listener({"channel": self._channel, "value": pwm, "min": self._pwm_offset, "max": self._pwm_limit, "type": "PWM"})

    def stop(self):
        self.update(0)


class ServoGroup(object):
    def __init__(self, servos):
        self._servos = servos.copy()
    
    def get(self, channel):
        for servo in self._servos:
            if servo._channel == channel:
                return servo
        return None

class PWMOutOfBoundsError(MotorError):
    def __init__(self, message="", expression=None):
        self.expression = expression
        self.message = message


class ChannelOutOfBoundsError(MotorError):
    def __init__(self, message="", expression=None):
        self.expression = expression
        self.message = message
