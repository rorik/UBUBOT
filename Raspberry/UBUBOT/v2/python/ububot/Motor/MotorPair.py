#!/usr/bin/python3
from ububot.Comms.Serial import SerialCommunication
from enum import Enum
from time import sleep


class MotorPairDirection(Enum):
    SHARP_LEFT = 0
    SHARP_RIGHT = 1


class MotorIdentifier(Enum):
    LEFT = 'L'
    RIGHT = 'R'
    BOTH = 'B'


class MotorPair(object):
    def __init__(self, result_listener=None):
        self._com = SerialCommunication()
        self._result_listener = result_listener

    def stop(self):
        self._com.send("STOP")
        if self._result_listener is not None:
            self._result_listener({"name": "stop"})

    def run(self, identifier, speed, time=None):
        if not isinstance(identifier, MotorIdentifier):
            raise InvalidIdentifierError(
                "Identifier must be of type MotorIdentifier")
        speed = round(speed, 2)
        if time is not None:
            time = round(time, 2)
            self._com.send("RNF;{};{};{}".format(
                identifier.value, speed, time))
            if self._result_listener is not None:
                self._result_listener({"name": "run_for", "identifier": identifier.value, "speed": speed, "time": time})
        else:
            self._com.send("RUN;{};{}".format(identifier.value, speed))
            if self._result_listener is not None:
                self._result_listener({"name": "run", "identifier": identifier.value, "speed": speed})

    def move_by(self, identifier, speed=200, angle=360):
        if not isinstance(identifier, MotorIdentifier):
            raise InvalidIdentifierError(
                "Identifier must be of type MotorIdentifier")
        speed = round(speed, 2)
        angle = round(angle, 2)
        self._com.send("MOVB;{};{};{}".format(identifier.value, speed, angle))
        if self._result_listener is not None:
            self._result_listener({"name": "move_by", "identifier": identifier.value, "speed": speed, "angle": angle})

    def move_to(self, identifier, speed=200, angle=360):
        if not isinstance(identifier, MotorIdentifier):
            raise InvalidIdentifierError(
                "Identifier must be of type MotorIdentifier")
        speed = round(speed, 2)
        angle = round(angle, 2)
        self._com.send("MOVT;{};{};{}".format(identifier.value, speed, angle))
        if self._result_listener is not None:
            self._result_listener({"name": "move_to", "identifier": identifier.value, "speed": speed, "angle": angle})

    def turn_sharp(self, direction, speed=200, angle=90):
        speed = round(speed, 2)
        angle = round(angle, 2)
        if direction is MotorPairDirection.SHARP_LEFT:
            self._com.send("MOVB;{};{};{}".format(
                MotorIdentifier.LEFT.value, speed, -angle))
            self._com.send("MOVB;{};{};{}".format(
                MotorIdentifier.RIGHT.value, speed, angle))
            if self._result_listener is not None:
                self._result_listener({"name": "turn_sharp", "direction": "left", "speed": speed, "angle": angle})
        elif direction is MotorPairDirection.SHARP_RIGHT:
            self._com.send("MOVB;{};{};{}".format(
                MotorIdentifier.LEFT.value, speed, angle))
            self._com.send("MOVB;{};{};{}".format(
                MotorIdentifier.RIGHT.value, speed, -angle))
            if self._result_listener is not None:
                self._result_listener({"name": "turn_sharp", "direction": "right", "speed": speed, "angle": angle})
        else:
            raise UnknownDirectionError(
                "Direction must be SHARP_LEFT or SHARP_RIGHT. Direction =", direction)

    def advance_cm(self, distance, speed=200, circumference=20.1):
        if distance == 0:
            self.stop()
        else:
            self.move_by(MotorIdentifier.BOTH, speed, distance/circumference*360)


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
