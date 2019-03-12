#!/usr/bin/python3
from Vision.Streamer import Streamer
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

resolution = (240, 512)
framerate = 12
delay = 0.2

with Streamer(delay) as streamer:
    with PiCamera() as camera:
        camera.resolution = resolution
        camera.framerate = framerate
        rawCapture = PiRGBArray(camera, size=resolution)
        time.sleep(0.1)
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            streamer.set_image(frame.array)
            rawCapture.truncate(0)
