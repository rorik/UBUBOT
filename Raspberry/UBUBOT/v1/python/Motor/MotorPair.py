#!/usr/bin/python3
import lib.RPi.GPIO as GPIO
import lib.PCA9685 as DRIVER
from Motor.Motor import Motor, MotorDirection, MotorError
from enum import Enum
from util.angle import cartesian_to_polar


class MotorPairDirection(Enum):
    STOP = 0
    FORWARDS = 1
    BACKWARDS = 2
    SHARP_LEFT = 3
    SHARP_RIGHT = 4
    VECTOR = 5
    POLAR = 6
    CARTESIAN = 7


class MotorPair(object):
    def __init__(self, config):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        driver = DRIVER.PWM(bus_number=config.I2CBus)
        driver.frequency = config.MotorDriverFrequency
        self.motor_left = Motor(driver, config.MotorDriverLeftPWM, config.MotorDriverLeftForwards,
                                config.MotorDriverLeftBackwards, factor=config.MotorLeftRatio)
        self.motor_right = Motor(driver, config.MotorDriverRightPWM, config.MotorDriverRightForwards,
                                 config.MotorDriverRightBackwards, factor=config.MotorRightRatio)

    def reduce(self, left=None, right=None, additive=False):
        if left is not None:
            if additive:
                self.motor_left.reduction += left
                if self.motor_left.reduction > 1:
                    self.motor_left.reduction = 1
            else:
                self.motor_left.reduction = left
            self.motor_left.update()
        if right is not None:
            if additive:
                self.motor_right.reduction += right
                if self.motor_right.reduction > 1:
                    self.motor_right.reduction = 1
            else:
                self.motor_right.reduction = right
            self.motor_right.update()

    def move(self, direction, speed=4095, speed_secondary=4095, angle=0.0, x=0, y=0, radius=4095):
        if speed < 0:
            print("WARNING: Using negative speed (", speed, ") on move(), absolute value used instead.", sep="")
            speed = -speed
        if direction == MotorPairDirection.STOP:
            self.stop()
        elif direction == MotorPairDirection.FORWARDS:
            self.straight(speed)
        elif direction == MotorPairDirection.BACKWARDS:
            self.straight(-speed)
        elif direction == MotorPairDirection.SHARP_LEFT:
            self.turn_sharp(-speed)
        elif direction == MotorPairDirection.SHARP_RIGHT:
            self.turn_sharp(speed)
        elif direction == MotorPairDirection.VECTOR:
            if speed == 0:
                self.move(MotorPairDirection.SHARP_RIGHT, speed_secondary)
            elif speed_secondary == 0:
                self.move(MotorPairDirection.SHARP_LEFT, speed)
            elif speed == speed_secondary:
                if speed > 0:
                    self.move(MotorPairDirection.FORWARDS, speed)
                elif speed < 0:
                    self.move(MotorPairDirection.BACKWARDS, speed)
                else:
                    self.stop()
            else:
                self.apply_vector(speed, speed_secondary)
        elif direction == MotorPairDirection.POLAR:
            angle %= 360
            if angle == 0:
                self.move(MotorPairDirection.FORWARDS, speed)
            elif angle == 90:
                self.move(MotorPairDirection.SHARP_LEFT, speed)
            elif angle == 180:
                self.move(MotorPairDirection.BACKWARDS, speed)
            elif angle == 270:
                self.move(MotorPairDirection.SHARP_RIGHT, speed)
            else:
                self.apply_polar(speed, angle)
        elif direction == MotorPairDirection.CARTESIAN:
            speed, angle = cartesian_to_polar(x, y, radius, 4095)
            self.move(MotorPairDirection.POLAR, speed=speed, angle=angle)
            return speed, angle
        else:
            raise UnknownDirectionError("Direction doesn't match any MotorPairDirection. Direction =", direction)

    def stop(self):
        self.motor_left.speed = 0
        self.motor_right.speed = 0
        self.motor_left.toggle(MotorDirection.STOP)
        self.motor_right.toggle(MotorDirection.STOP)

    def straight(self, speed=4095):
        self.apply_vector(speed, speed)

    def turn_sharp(self, left_speed=4095):
        self.apply_vector(left_speed, -left_speed)

    def apply_vector(self, left_speed, right_speed):
        self.motor_left.update(left_speed)
        self.motor_right.update(right_speed)

    def apply_polar(self, speed, angle):
        if angle % 90 == 45:
            if angle == 45:
                self.apply_vector(speed / 3, speed)
            elif angle == 315:
                self.apply_vector(speed, speed / 3)
        pass

    def lock(self, direction=MotorDirection.STOP):
        self.motor_left.locked = direction
        self.motor_right.locked = direction
        self.motor_left.update()
        self.motor_right.update()


class UnknownDirectionError(MotorError):
    def __init__(self, message="", expression=None):
        self.expression = expression
        self.message = message
