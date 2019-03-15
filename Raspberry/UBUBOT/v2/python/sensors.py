#!/usr/bin/python3
from Sensor.IR import SensorEvent
from Sensor.SensorGroup import CardinalPosition
from util.Initializer import UBUBOT
from time import sleep
from sys import stdout

def callback(pin):
    for position in remaining:
        if ububot.sensors.get(position)._pin == pin:
            remaining.remove(position)
            break

if __name__ == '__main__':

    with UBUBOT(sensors=True) as ububot:
        remaining = [position for position in CardinalPosition]

        ububot.sensors.get_east().add_callback(SensorEvent.DETECT_START, callback)
        ububot.sensors.get_north().add_callback(SensorEvent.DETECT_START, callback)
        ububot.sensors.get_south().add_callback(SensorEvent.DETECT_START, callback)
        ububot.sensors.get_west().add_callback(SensorEvent.DETECT_START, callback)
        while len(remaining) > 0:
            print("Remaining:", ", ".join([position.name for position in remaining]))
            sleep(0.1)
            stdout.write("\033[F\033[K")
