#!/usr/bin/python3
from ububot.Vision.Streamer import Streamer
from ububot.Vision.CameraStream import CameraStream
from ububot.Vision.Line import get_sections, draw_sections, get_stops, get_paths, draw_paths

#resolution = (320, 240)
resolution = (640, 480)
#resolution = (1640, 1232)
framerate = 10
socket_interval = 0.2
color_threshold = 50
precision = 5


def process_image(image):
    sections = get_sections(image, threshold=color_threshold, precision=precision)
    sections.pop(max(sections.keys()))
    draw_sections(image, sections)
    draw_paths(image, get_paths(sections))
    draw_sections(image, get_stops(sections, 50), color=(200, 200, 200))
    streamer.set_image(image)


if __name__ == "__main__":
    with Streamer(socket_interval) as streamer, CameraStream(resolution, framerate) as capture_stream:
        capture_stream.add_callback(process_image)
        try:
            capture_stream.join()
        except KeyboardInterrupt:
            pass
