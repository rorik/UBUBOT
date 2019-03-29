#!/usr/bin/python3
from ububot.Initializer import UBUBOT
from ububot.Motor.MotorPair import MotorIdentifier, MotorPairDirection
from argparse import ArgumentParser
from time import sleep
from enum import Enum


grid = [
    #A.x  B.x  C.x  D.x  E.x  F.x  G.x, H.x
    [100, 300, 200, 150, 400, 230, 180, 100],
    #6.y  5.y  4.y  3.y  2.y, 1.y, A.y
    [100, 135, 175, 215, 255, 295, 100]
]


class Direction(Enum):
    UP = [0, 1, 0]
    RIGHT = [1, 0, 90]
    DOWN = [0, -1, 180]
    LEFT = [-1, 0, 270]


def turn(ububot, current, target):
    if current is not target:
        arch = target.value[2] - current.value[2]
        if arch > 180:
            arch = arch - 360
        elif arch <= -180:
            arch = arch + 360
        print('TURN', arch)
        #TODO: move
    return target


def advance(ububot, position, direction):
    index = abs(direction.value[1])
    distance = grid[index][position[index] +
                           int((1 + direction.value[index]) / 2)]
    position[index] += direction.value[index]
    print('ADVANCE', distance, '=>', position)
    #TODO: move


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('start', nargs='?', type=int, default=1)
    parser.add_argument('end', nargs='?', type=str, default='m')
    args = parser.parse_args()
    args.end = args.end.lower()

    assert 1 <= args.start <= 13
    assert len(args.end) == 1 and 'a' <= args.end <= 'm'

    remaining = []
    if args.start > 6:
        start = [args.start - 7, -1]
        direction = Direction.UP
    else:
        start = [-1, 6 - args.start]
        direction = Direction.RIGHT

    if args.end < 'g':
        remaining.append([ord(args.end) - ord('a'), 5])
        end = [ord(args.end) - ord('a'), 6]
    else:
        remaining.append([6, ord('m') - ord(args.end)])
        end = [7, ord('m') - ord(args.end)]

    remaining.append(end)
    position = start.copy()

    with UBUBOT(motors=True) as ububot:
        print('== PATH ==')
        print(" => ".join([str(position) for position in [start] + remaining]))
        print('==========')
        advance(ububot, position, direction)
        while len(remaining) > 0:
            for i in range(100):
                if position[0] != remaining[0][0]:
                    if position[0] > remaining[0][0]:
                        direction = turn(ububot, direction, Direction.LEFT)
                    else:
                        direction = turn(ububot, direction, Direction.RIGHT)
                    advance(ububot, position, direction)
                elif position[1] != remaining[0][1]:
                    if position[1] < remaining[0][1]:
                        direction = turn(ububot, direction, Direction.UP)
                    else:
                        direction = turn(ububot, direction, Direction.DOWN)
                    advance(ububot, position, direction)
                else:
                    print('REACHED TARGET', remaining[0])
                    remaining.pop(0)
                    break
