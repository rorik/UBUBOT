#!/usr/bin/python3
from Comms.Serial import SerialCommunication
from enum import Enum


class MotorPairDirection(Enum):
    SHARP_LEFT = 0
    SHARP_RIGHT = 1

class MotorIdentifier(Enum):
    LEFT = 'L'
    RIGHT = 'R'
    BOTH = 'B'


class MotorPair(object):
    def __init__(self):
        self._com = SerialCommunication()

    def stop(self):
        self._com.send("STOP")
        
    def run(self, identifier, speed, time=None):
        if not isinstance(identifier, MotorIdentifier):
            raise InvalidIdentifierError("Identifier must be of type MotorIdentifier")
        if time is not None:
            self._com.send("RNF;{};{};{}".format(identifier.value, speed, time))
        else:
            self._com.send("RUN;{};{}".format(identifier.value, speed))

    def move_by(self, identifier, speed=200, angle=360):
        if not isinstance(identifier, MotorIdentifier):
            raise InvalidIdentifierError("Identifier must be of type MotorIdentifier")
        self._com.send("MOVB;{};{};{}".format(identifier.value, speed, angle))

    def move_to(self, identifier, speed=200, angle=360):
        if not isinstance(identifier, MotorIdentifier):
            raise InvalidIdentifierError("Identifier must be of type MotorIdentifier")
        self._com.send("MOVT;{};{};{}".format(identifier.value, speed, angle))

    def turn_sharp(self, direction, speed=200, angle=90):
        if direction is MotorPairDirection.SHARP_LEFT:
            self._com.send("MOVB;{};{};{}".format(MotorIdentifier.LEFT.value, -speed, angle))
            self._com.send("MOVB;{};{};{}".format(MotorIdentifier.RIGHT.value, speed, angle))
        elif direction is MotorPairDirection.SHARP_RIGHT:
            self._com.send("MOVB;{};{};{}".format(MotorIdentifier.LEFT.value, speed, angle))
            self._com.send("MOVB;{};{};{}".format(MotorIdentifier.RIGHT.value, -speed, angle))
        else:
            raise UnknownDirectionError("Direction must be SHARP_LEFT or SHARP_RIGHT. Direction =", direction)

    def advance_cm(self, distance, speed=200, circumference=20.42):
        if distance > 0:
            self.move_by(MotorIdentifier.BOTH, speed, distance/circumference)
        elif distance < 0:
            self.move_by(MotorIdentifier.BOTH, -speed, -distance/circumference)
        else:
            self.stop()


class MotorError(Exception):
    pass


class UnknownDirectionError(MotorError):
    def __init__(self, message="", expression=None):
        self.expression = expression
        self.message = message

class InvalidIdentifierError(MotorError):
    def __init__(self, message="", expression=None):
        self.expression = expression
        self.message = message

