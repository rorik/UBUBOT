#!/usr/bin/python3
from ububot.Initializer import UBUBOT
from ububot.Motor.MotorPair import MotorIdentifier, MotorPairDirection
from ububot.Vision.Streamer import Streamer
from ububot.Vision.CameraStream import CameraStream
from ububot.Vision.LineFollower import LineFollower
from ububot.Vision.Line import draw_sections, draw_paths, draw_line, midpoint, get_stops, get_sections
from argparse import ArgumentParser
from time import sleep
from enum import Enum

speed=30
turn_speed=100
advance_distance=6
resolution=(640, 480)
framerate=8
precision = 5

# Stops config
stop_threshold=45
min_y = -20
max_y = 20
dotted = [[i, (i+10)] for i in range(0, 100, 30)]

# Colors config
dotted_color = (0, 0, 150)
sections_color = (0, 255, 0)
stops_color = (0, 255, 255)
paths_color = (255, 255, 0)
vector_color = (255, 0, 0)

class Direction(Enum):
    UP = [0, 1, 0]
    RIGHT = [1, 0, 90]
    DOWN = [0, -1, 180]
    LEFT = [-1, 0, 270]

def follower_callback(img, sections, stops, paths, current_path, vector):
    draw_sections(img, {min_y: dotted, max_y: dotted}, dotted_color)
    draw_sections(img, sections)
    if stops is not None:
        draw_sections(img, stops, stops_color)
    if paths is not None:
        draw_paths(img, paths, paths_color)
        if vector is not None:
            draw_line(img, midpoint(*current_path[0][1]), current_path[0][0] + 50,
                    midpoint(*current_path[-1][1]), current_path[-1][0] + 50, vector_color)
    streamer.set_image(img)

def turn(ububot, current, target):
    if current is not target:
        arch = target.value[2] - current.value[2]
        if arch > 180:
            arch = arch - 360
        elif arch <= -180:
            arch = arch + 360
        print("TURN", arch)
        ububot.motors.turn_sharp(MotorPairDirection.SHARP_RIGHT, speed=turn_speed, angle=arch)
    return target


def advance(ububot: UBUBOT, position, direction, follower: LineFollower):
    index = abs(direction.value[1])
    position[index] += direction.value[index]
    print("ADVANCE =>", position)
    stops = get_stops(get_sections(camera.wait_for_capture(), precision=precision))
    for relative_y, sections in stops.items():
            if min_y <= relative_y <= max_y and len(sections) > 0:
                ububot.motors.advance_cm(advance_distance, speed)
                sleep(1)
    follower._follow(ububot.motors, speed=speed, min_y=min_y, max_y=max_y, stop_threshold=stop_threshold, timeout=2, callback=follower_callback)    


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

    with UBUBOT(motors=True, motors_socket=True, serial_socket_capture=True, status_socket=True) as ububot, \
            Streamer(0.5) as streamer, \
            CameraStream(resolution=resolution, framerate=framerate) as camera, \
            LineFollower(camera, precision=precision) as follower:
        print('== PATH ==')
        print(" => ".join([str(position) for position in [start] + remaining]))
        print('==========')
        advance(ububot, position, direction, follower)
        while len(remaining) > 0:
            for i in range(100):
                if position[0] != remaining[0][0]:
                    if position[0] > remaining[0][0]:
                        direction = turn(ububot, direction, Direction.LEFT)
                    else:
                        direction = turn(ububot, direction, Direction.RIGHT)
                    advance(ububot, position, direction, follower)
                elif position[1] != remaining[0][1]:
                    if position[1] < remaining[0][1]:
                        direction = turn(ububot, direction, Direction.UP)
                    else:
                        direction = turn(ububot, direction, Direction.DOWN)
                    advance(ububot, position, direction, follower)
                else:
                    print('REACHED TARGET', remaining[0])
                    remaining.pop(0)
                    break
