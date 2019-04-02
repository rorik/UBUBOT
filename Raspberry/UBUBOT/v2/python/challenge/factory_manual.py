#!/usr/bin/python3
from ububot.Initializer import UBUBOT
from ububot.Vision.CameraStream import CameraStream
from ububot.Vision.LineFollower import LineFollower
from ububot.Vision.Line import draw_sections, draw_paths, draw_line, midpoint
from ububot.Vision.Streamer import Streamer
from ububot.Motor.MotorPair import MotorPairDirection
from time import sleep
from sys import stdin, stdout
from tty import setraw
from termios import tcgetattr, tcsetattr, TCSADRAIN

# Factory config
speed = 20
turn_speed = 100
turn_factor = 2.3
claw_channel = 7
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

def getChar():
    fd = stdin.fileno()
    old_settings = tcgetattr(fd)
    try:
        setraw(stdin.fileno())
        ch = stdin.read(1)
    finally:
        tcsetattr(fd, TCSADRAIN, old_settings)
    return ch

if __name__ == '__main__':
    with UBUBOT(motors=True, servos=True, relays=True, sensors=True, motors_socket=True, serial_socket_capture=True, status_socket=True) as ububot, \
            Streamer(0.5) as streamer, \
            CameraStream(resolution=resolution, framerate=framerate) as camera, \
            LineFollower(camera, precision=precision) as follower:
        print("Controls:")
        print("- w : go to the next stop")
        print("- a : turn left")
        print("- d : turn right")
        print("- q : sharp left")
        print("- e : sharp right")
        print("- s : reverse 2cm")
        print("- x : toggle claw")
        print("- c : change light state")
        print("- 1 : open gate")
        print("- 2 : close gate")
        print("- p : finish")
        claw = True
        key = getChar()
        while not (key == '\r' or key == '\n' or key == 'p'):
            if key == 'w':
                response = follower.follow(ububot.motors, speed=speed, stop_threshold=stop_threshold, min_y=min_y, max_y=max_y, timeout=20, callback=follower_callback)
                print(response)
            elif key == 's':
                ububot.motors.advance_cm(-2, speed)
            elif key == 'a':
                ububot.motors.advance_cm(24, turn_speed)
                sleep(1)
                ububot.motors.turn_sharp(MotorPairDirection.SHARP_LEFT, turn_speed, 90*turn_factor)
                sleep(1)
                ububot.motors.advance_cm(12, turn_speed)
            elif key == 'd':
                ububot.motors.advance_cm(24, turn_speed)
                sleep(1)
                ububot.motors.turn_sharp(MotorPairDirection.SHARP_RIGHT, turn_speed, 90*turn_factor)
                sleep(1)
                ububot.motors.advance_cm(12, turn_speed)
            elif key == 'q':
                ububot.motors.turn_sharp(MotorPairDirection.SHARP_LEFT, turn_speed, 90*turn_factor)
            elif key == 'e':
                ububot.motors.turn_sharp(MotorPairDirection.SHARP_RIGHT, turn_speed, 90*turn_factor)
            elif key == 'x':
                ububot.servos.get(claw_channel).angle(0 if claw else 120)
                claw = not claw
            elif key == 'c':
                ububot.relays.get_light().off()
                sleep(0.1)
                ububot.relays.get_light().on()
            elif key == '1':
                pass # TODO
            elif key == '2':
                pass # TODO
            key = getChar()
        ububot.motors.stop()
        input('Press enter to end...')
