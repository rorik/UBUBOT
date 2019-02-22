#!/usr/bin/python3
from Motor.MotorPair import MotorPair, MotorPairDirection, MotorIdentifier
from Sensor.IR import IRSensor
from Sensor.SensorGroup import CardinalGroup

def initialize():
    return MotorPair(), CardinalGroup(north=IRSensor(12), south=IRSensor(16), west=IRSensor(18), east=IRSensor(22))