#!/usr/bin/python3
import math


def cartesian_to_polar(x, y, max_radius=32768, expected_radius=4095):
    distance = int(int(math.sqrt(pow(x, 2) + pow(y, 2))) / max_radius * expected_radius)
    if distance > 4095:
        distance = 4095
    if x == 0:
        angle = 0 if y > 0 else 180
    else:
        angle = math.degrees(math.atan(y / x))
        if x < 0:
            angle = (angle + 90)
        else:
            angle = (angle - 90)
    return distance, angle
