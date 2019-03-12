#!/usr/bin/python3
from Vision.Streamer import Streamer
from Vision.Analysis import get_sections, draw_sections
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

resolution = (240, 512)
framerate = 12
socket_interval = 0.2

if __name__ == "__main__":

    with Streamer(socket_interval) as streamer, PiCamera() as camera:
        camera.resolution = resolution
        camera.framerate = framerate
        rawCapture = PiRGBArray(camera, size=resolution)
        time.sleep(0.1)
        try:
            for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
                image = frame.array
                draw_sections(image, get_sections(image, 5))
                streamer.set_image(image)
                rawCapture.truncate(0)
        except KeyboardInterrupt:
            pass
