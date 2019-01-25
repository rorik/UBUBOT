import RPi.GPIO as GPIO
import lib.PCA9685 as DRIVER


class MotorDirection:
    STOP = 0
    FORWARDS = 1
    BACKWARDS = 2


class Motor(object):
    direction = MotorDirection.STOP

    def __init__(self, driver, pin_forwards, pin_backwards, factor=1.0, speed=0, frequency=60, bus=1):
        if not -1.0 <= factor <= 1.0:
            raise FactorOutOfBoundsError("Factor = " + str(factor) + ". MAXIMUM = +/- 1")
        if frequency < 1:
            raise FrequencyOutOfBoundsError("Frequency = " + str(frequency) + ". MINIMUM = 1")
        self.factor = factor
        self.speed = speed
        self.pin_forwards = pin_forwards
        self.pin_backwards = pin_backwards
        self.pwm = DRIVER.PWM(bus_number=bus)
        self.pwm.frequency = frequency
        self.driver = driver
        GPIO.setup(pin_forwards, GPIO.OUT)
        GPIO.setup(pin_backwards, GPIO.OUT)
        GPIO.output(pin_forwards, speed > 0)
        GPIO.output(pin_backwards, speed < 0)

    def toggle(self, direction):
        self.direction = direction
        GPIO.output(self.pin_forwards, direction == MotorDirection.FORWARDS)
        GPIO.output(self.pin_backwards, direction == MotorDirection.BACKWARDS)

    def update(self, speed=None):
        if speed is not None:
            self.speed = speed
        if abs(self.speed) > 4095:
            raise SpeedOutOfBoundsError("Speed = " + str(self.speed) + ". MAXIMUM = +/- " +
                                        (str(4095) if abs(self.factor) <= 1 else str(4095/self.factor)))
        if self.speed == 0:
            if self.direction != MotorDirection.STOP:
                self.toggle(MotorDirection.STOP)
        elif self.speed > 0:
            if self.direction != MotorDirection.FORWARDS:
                self.toggle(MotorDirection.FORWARDS)
        else:
            if self.direction != MotorDirection.BACKWARDS:
                self.toggle(MotorDirection.BACKWARDS)
        self.pwm.write(self.driver, 0, abs(int(self.speed * self.factor)))


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
