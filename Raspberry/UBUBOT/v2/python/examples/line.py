#!/usr/bin/python3
from ububot.Initializer import UBUBOT
from ububot.Vision.CameraStream import CameraStream
from ububot.Vision.LineFollower import LineFollower
from ububot.Vision.Line import draw_all, draw_sections
from ububot.Vision.Streamer import Streamer
from time import sleep

min_y = -20
max_y = 20


def process_image(image):
    img = image.copy()
    draw_sections(img, {min_y: [[0, 100]], max_y: [[0, 100]]})
    draw_all(img)
    streamer.set_image(img)

if __name__ == '__main__':
    with UBUBOT(motors=True, relays=True, sensors=True, serial_socket_capture=True, status_socket=True) as ububot, CameraStream() as camera, Streamer(0.5) as streamer, LineFollower(camera) as follower:
            camera.add_callback(process_image)
            sleep(1)
            input("Press Enter to continue...")
            follower.follow(ububot.motors, min_y=min_y, max_y=max_y, timeout=20)
            ububot.motors.stop()
