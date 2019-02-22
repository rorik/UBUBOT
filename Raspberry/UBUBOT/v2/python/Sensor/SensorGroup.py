#!/usr/bin/python3
from enum import Enum

class CardinalPosition(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

class CardinalGroup(object):
    def __init__(self, north=None, south=None, west=None, east=None):
        self._north = north
        self._south = south
        self._west = west
        self._east = east

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
    