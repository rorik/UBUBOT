#!/usr/bin/python3
from ububot.Relay.Relay import Relay
from enum import Enum
import RPi.GPIO as GPIO


class FunctionalIdentifier(Enum):
    LIGHT = 0
    BUZZER = 1
    MOTOR_1 = 2
    MOTOR_2 = 3


class FunctionalGroup(object):
    _light: Relay
    _buzzer: Relay
    _motor_1: Relay
    _motor_2: Relay
    
    def __init__(self, light=None, buzzer=None, motor_1=None, motor_2=None, state_listener=None):
        if light is None or isinstance(light, Relay):
            self._light = light
        else:
            self._light = Relay(light, state_listener=state_listener, name=FunctionalIdentifier.LIGHT.name)

        if buzzer is None or isinstance(buzzer, Relay):
            self._buzzer = buzzer
        else:
            self._buzzer = Relay(buzzer, state_listener=state_listener, name=FunctionalIdentifier.BUZZER.name)

        if motor_1 is None or isinstance(motor_1, Relay):
            self._motor_1 = motor_1
        else:
            self._motor_1 = Relay(motor_1, state_listener=state_listener, name=FunctionalIdentifier.MOTOR_1.name)

        if motor_2 is None or isinstance(motor_2, Relay):
            self._motor_2 = motor_2
        else:
            self._motor_2 = Relay(motor_2, state_listener=state_listener, name=FunctionalIdentifier.MOTOR_2.name)
        
        for identifier in FunctionalIdentifier:
            relay = self.get(identifier)
            if relay is not None:
                relay.set_name(identifier.name)

    def get(self, identifier):
        if identifier == FunctionalIdentifier.LIGHT:
            return self.get_light()
        elif identifier == FunctionalIdentifier.BUZZER:
            return self.get_buzzer()
        elif identifier == FunctionalIdentifier.MOTOR_1:
            return self.get_motor_1()
        elif identifier == FunctionalIdentifier.MOTOR_2:
            return self.get_motor_2()
        else:
            raise ValueError("Unknown identifier ({})".format(identifier))

    def get_light(self):
        return self._light

    def get_buzzer(self):
        return self._buzzer

    def get_motor_1(self):
        return self._motor_1

    def get_motor_2(self):
        return self._motor_2

    def on(self):
        self.set_state(GPIO.HIGH)

    def off(self):
        self.set_state(GPIO.LOW)

    def set_state(self, state):
        for relay in [self.get(identifier) for identifier in FunctionalIdentifier]:
            if relay is not None:
                relay.set_state(state)
