#!/usr/bin/python3


class Config(object):
    I2CBus = None
    Handshake = None
    PiCamEnabled = None
    UltraSonicMode = None
    UltraSonicLock = None
    MotorLeftRatio = None
    MotorRightRatio = None
    UltraSonicState = None
    UltraSonicAddress = None
    MotorDriverLeftPWM = None
    MotorDriverRightPWM = None
    UltraSonicThreshold = None
    MotorDriverFrequency = None
    UltraSonicPollingRate = None
    UltraSonicPollingDelay = None
    UltraSonicInterruptPin = None
    MotorDriverLeftForwards = None
    MotorDriverLeftBackwards = None
    MotorDriverRightForwards = None
    MotorDriverRightBackwards = None
    UltraSonicInterruptPinEnabled = None

    def __init__(self, apply_defaults=True):
        if apply_defaults:
            self.I2CBus = 1
            self.Handshake = True
            self.PiCamEnabled = False
            self.UltraSonicMode = 3
            self.UltraSonicLock = True
            self.MotorLeftRatio = 1
            self.MotorRightRatio = 1
            self.UltraSonicState = 0
            self.UltraSonicAddress = 0x10
            self.MotorDriverLeftPWM = 15
            self.MotorDriverRightPWM = 14
            self.UltraSonicThreshold = 7
            self.MotorDriverFrequency = 100
            self.UltraSonicPollingRate = 6
            self.UltraSonicPollingDelay = 2
            self.UltraSonicInterruptPin = 7
            self.MotorDriverLeftForwards = 11
            self.MotorDriverLeftBackwards = 10
            self.MotorDriverRightForwards = 9
            self.MotorDriverRightBackwards = 8
            self.UltraSonicInterruptPinEnabled = True

    def verify(self):
        for var in vars(self):
            if var is None:
                raise UnfinishedConfigError


class ConfigError(Exception):
    pass


class UnfinishedConfigError(ConfigError):
    def __init__(self, message="", expression=None):
        self.expression = expression
        self.message = message
