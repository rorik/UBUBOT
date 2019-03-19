#!/usr/bin/python3
from enum import Enum
from Sensor.IR import IRSensor

class CardinalPosition(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

class CardinalGroup(object):
    def __init__(self, north=None, south=None, west=None, east=None, state_listener=None):
        if north is None or isinstance(north, IRSensor):
            self._north = north
        else:
            self._north = IRSensor(north, state_listener=state_listener, name=CardinalPosition.NORTH.name)
        
        if south is None or isinstance(south, IRSensor):
            self._south = south
        else:
            self._south = IRSensor(south, state_listener=state_listener, name=CardinalPosition.SOUTH.name)

        if west is None or isinstance(west, IRSensor):
            self._west = west
        else:
            self._west = IRSensor(west, state_listener=state_listener, name=CardinalPosition.WEST.name)
        
        if east is None or isinstance(east, IRSensor):
            self._east = south
        else:
            self._east = IRSensor(east, state_listener=state_listener, name=CardinalPosition.EAST.name)
        
        for identifier in CardinalPosition:
            sensor = self.get(identifier)
            if sensor is not None:
                sensor.set_name(identifier.name)

    def get(self, position):
        if position == CardinalPosition.NORTH:
            return self.get_north()
        elif position == CardinalPosition.EAST:
            return self.get_east()
        elif position == CardinalPosition.SOUTH:
            return self.get_south()
        elif position == CardinalPosition.WEST:
            return self.get_west()
        else:
            raise ValueError("Unknown position ({})".format(position))
    
    def get_north(self):
        return self._north
    
    def get_south(self):
        return self._south
    
    def get_west(self):
        return self._west
    
    def get_east(self):
        return self._east
    