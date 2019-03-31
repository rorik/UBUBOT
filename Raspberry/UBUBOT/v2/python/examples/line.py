#!/usr/bin/python3
from ububot.Initializer import UBUBOT
from ububot.Vision.CameraStream import CameraStream
from ububot.Vision.LineFollower import LineFollower
from ububot.Vision.Line import draw_sections, draw_paths, draw_line
from ububot.Vision.Streamer import Streamer
from time import sleep

min_y = -20
max_y = 20

def follower_callback(img, sections, stops, paths, current_path, vector):
    draw_sections(img, sections)
    draw_sections(img, {min_y: [[i, (i+10)] for i in range(0, 100, 30)], max_y: [[i, (i+10)] for i in range(0, 100, 30)]}, (0, 0, 200))
    if stops is not None:
        draw_sections(img, stops, (120, 120, 120))
    draw_paths(img, paths)
    if vector is not None:
        draw_line(img, sum(current_path[0][1]) / 2, current_path[0][0] + 50, sum(current_path[-1][1]) / 2, current_path[-1][0] + 50, (200, 100, 50))
    streamer.set_image(img)

if __name__ == '__main__':
    with UBUBOT(motors=True, relays=True, sensors=True, serial_socket_capture=True, status_socket=True) as ububot, CameraStream() as camera, Streamer(0.5) as streamer, LineFollower(camera) as follower:
            sleep(1)
            input("Press Enter to continue...")
            follower.follow(ububot.motors, stop_threshold=60, min_y=min_y, max_y=max_y, timeout=20, callback=follower_callback)
            ububot.motors.stop()
