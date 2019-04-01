#!/usr/bin/python3
from ububot.Initializer import UBUBOT
from ububot.Vision.CameraStream import CameraStream
from ububot.Vision.LineFollower import LineFollower
from ububot.Vision.Line import draw_sections, draw_paths, draw_line, midpoint
from ububot.Vision.Streamer import Streamer
from time import sleep

min_y = -20
max_y = 20
dotted = [[i, (i+10)] for i in range(0, 100, 30)]

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
    draw_paths(img, paths, paths_color)
    if vector is not None:
        draw_line(img, midpoint(*current_path[0][1]), current_path[0][0] + 50,
                  midpoint(*current_path[-1][1]), current_path[-1][0] + 50, vector_color)
    streamer.set_image(img)


if __name__ == '__main__':
    with UBUBOT(motors=True, relays=True, sensors=True, serial_socket_capture=True, status_socket=True) as ububot, \
            Streamer(0.5) as streamer, \
            LineFollower(CameraStream()) as follower:
        sleep(1)
        input("Press Enter to continue...")
        follower.follow(ububot.motors, stop_threshold=60, min_y=min_y,
                        max_y=max_y, timeout=20, callback=follower_callback)
        ububot.motors.stop()
