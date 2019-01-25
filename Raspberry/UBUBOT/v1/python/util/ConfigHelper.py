#!/usr/bin/python3
import configparser
from util.Config import Config as Config, ConfigError


class ConfigHelper(object):
    def __init__(self, path=None, config=None, apply_defaults=True, verify=True):
        if config is None:
            if path is None:
                self.config = Config(apply_defaults)
            else:
                self.config = self.load_config(path)
        if verify:
            self.config.verify()

    @staticmethod
    def load_config(path):
        configuration = Config(False)
        configFile = configparser.ConfigParser()
        try:
            configFile.read(path)
            with open(path) as f:
                configFile.read_file(f)
        except IOError as error:
            print("File at \"", path, "\" not found.", sep="")
            raise error
        try:
            # Main
            ratio = float(configFile.get("Main", "LeftToRightRatio"))
            if not 0 <= ratio <= 2:
                raise configparser.ParsingError("LeftToRightRatio out of bounds ({:.3f} OOR [0,2])".format(ratio))
            if ratio <= 1:
                configuration.MotorLeftRatio = ratio
                configuration.MotorRightRatio = 1
            else:
                configuration.MotorLeftRatio = 1
                configuration.MotorRightRatio = 1 / ratio
            configuration.PiCamEnabled = configFile.get("Main", "CamEnabled").lower() == "true"
            configuration.I2CBus = int(configFile.get("Main", "i2cBus"))
            if not 0 <= configuration.I2CBus <= 2:
                raise configparser.ParsingError("Bus out of bounds ({:d} OOR [0,2])".format(configuration.I2CBus))
            configuration.MotorDriverFrequency = int(configFile.get("Main", "MotorDriverFrequency"))
            if not 1 <= configuration.MotorDriverFrequency <= 10000:
                raise configparser.ParsingError(
                    "Frequency out of bounds ({:d} OOR [1,10000])".format(configuration.MotorDriverFrequency))
            configuration.Handshake = configFile.get("Main", "Handshake").lower() == "true"

            # Sensors
            configuration.UltraSonicState = int(configFile.get("Sensors", "USMode"))
            configuration.UltraSonicInterruptPinEnabled = configFile.get("Sensors", "USInterruptPin").lower() == "true"
            configuration.UltraSonicMode = int(configFile.get("Sensors", "USPollingMethod"))
            if not 0 <= configuration.UltraSonicMode <= 4:
                raise configparser.ParsingError("Method {:d} not recognized".format(configuration.UltraSonicMode))
            configuration.UltraSonicLock = configFile.get("Sensors", "USLock").lower() == "true"
            if configuration.UltraSonicLock and configuration.UltraSonicMode == 0:
                raise configparser.ParsingError("US Lock is enabled but there is no polling method")
            configuration.UltraSonicThreshold = int(configFile.get("Sensors", "USDistanceInterrupt"))
            if configuration.UltraSonicThreshold < 0:
                raise configparser.ParsingError(
                    "Distance cannot be negative ({:d} < 0)".format(configuration.UltraSonicThreshold))
            if configuration.UltraSonicMode == 2 and configuration.UltraSonicThreshold > 29:
                raise configparser.ParsingError(
                    "Threshold out of bounds ({:d} OOR [0,29])".format(configuration.UltraSonicThreshold))
            configuration.UltraSonicPollingRate = int(configFile.get("Sensors", "USPollingRate"))
            if configuration.UltraSonicMode != 3 and not 1 <= configuration.UltraSonicPollingRate <= 100:
                raise configparser.ParsingError(
                    "Polling rate out of bounds ({:d} OOR [1,100])".format(configuration.UltraSonicPollingRate))
            configuration.UltraSonicPollingDelay = float(configFile.get("Sensors", "USDelay"))
            if configuration.UltraSonicMode != 3 and configuration.UltraSonicPollingDelay <= 0:
                raise configparser.ParsingError(
                    "Delay must be positive number ({:.2f} <= 0)".format(configuration.UltraSonicPollingDelay))

            # Pins
            configuration.UltraSonicInterruptPin = int(configFile.get("Pins", "InterruptPin"))
            configuration.MotorDriverLeftPWM = int(configFile.get("Pins", "MotorDriverLeftPWM"))
            configuration.MotorDriverRightPWM = int(configFile.get("Pins", "MotorDriverRightPWM"))
            configuration.MotorDriverLeftForwards = int(configFile.get("Pins", "MotorDriverLeftForwards"))
            configuration.MotorDriverLeftBackwards = int(configFile.get("Pins", "MotorDriverLeftBackwards"))
            configuration.MotorDriverRightForwards = int(configFile.get("Pins", "MotorDriverRightForwards"))
            configuration.MotorDriverRightBackwards = int(configFile.get("Pins", "MotorDriverRightBackwards"))
        except configparser.Error as error:
            print("Config file {} contains errors.".format(path))
            raise error
        return configuration

    @staticmethod
    def handshake(config):
        import smbus
        import time
        bus = smbus.SMBus(config.I2CBus)
        enabled = 1 if config.UltraSonicInterruptPinEnabled else 0
        read = bus.read_byte_data(0x10, 50 + enabled)
        if read != enabled:
            raise HandshakeError(
                "Handshake failed at setting interrupt pin, sent={:d} received={:d}".format(enabled + 50, read))
        time.sleep(config.UltraSonicPollingDelay/1000)

        enabled = 0 if config.UltraSonicState == 2 else 1
        read = bus.read_byte_data(0x10, 54 + enabled)
        if read != enabled:
            raise HandshakeError(
                "Handshake failed at setting sensor state, sent={:d} received={:d}".format(enabled + 54, read))
        time.sleep(config.UltraSonicPollingDelay/1000)

        if config.UltraSonicThreshold < 29:
            distance = config.UltraSonicThreshold
            read = bus.read_byte_data(0x10, distance + 60)
        else:
            distance = int((config.UltraSonicThreshold - 30) / 5)
            read = bus.read_byte_data(0x10, distance + 90)
            distance *= 5

        if read != distance:
            raise HandshakeError(
                "Handshake failed at setting threshold, sent={:d} received={:d}".format(distance, read))


class HandshakeError(ConfigError):
    def __init__(self, message="", expression=None):
        self.expression = expression
        self.message = message
