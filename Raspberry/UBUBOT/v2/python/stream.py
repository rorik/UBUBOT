#!/usr/bin/python3
from Vision.Streamer import Streamer
from Vision.CameraStream import CameraStream
from Vision.Analysis import get_sections, draw_sections
from Vision.Line import get_stops, get_paths, draw_paths

resolution = (240, 512)
framerate = 10
socket_interval = 0.2


def process_image(image):
    sections = get_sections(image, 5)
    sections.pop(50)
    draw_sections(image, sections)
    stops = get_stops(sections)
    draw_sections(image, stops, (255, 0, 0))
    paths = get_paths(sections)
    draw_paths(image, paths)
    streamer.set_image(image)


if __name__ == "__main__":
    with Streamer(socket_interval) as streamer, CameraStream(resolution, framerate) as capture_stream:
        capture_stream.add_callback(process_image)
        try:
            capture_stream.join()
        except KeyboardInterrupt:
            pass
