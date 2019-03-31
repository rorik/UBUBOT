#!/usr/bin/python3
from threading import Thread, Timer, Event
from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep


class CameraStream(Thread):
    def __init__(self, resolution=(240, 512), framerate=6, callback=None):
        super(CameraStream, self).__init__()
        self._capture_avaiable = Event()
        self._image = None
        self._stop_flag = False
        self._resolution = resolution
        self._framerate = framerate
        if callback is not None:
            self._callbacks = [callback]
        else:
            self._callbacks = []

    def get_image(self):
        return self._image

    def add_callback(self, callback):
        self._callbacks.append(callback)
    
    def wait_for_capture(self, timeout=None):
        if self._capture_avaiable.wait(timeout):
            return self._image
        return None

    def run(self):
        with PiCamera() as camera:
            camera.resolution = self._resolution
            camera.framerate = self._framerate
            camera.color_effects = (128, 128)
            rawCapture = PiRGBArray(camera, size=self._resolution)
            sleep(0.1)
            for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
                self._image = frame.array
                self._capture_avaiable.set()
                for callback in self._callbacks:
                    callback(self._image)
                rawCapture.truncate(0)
                self._capture_avaiable.clear()
                if self._stop_flag:
                    break

    def finalize(self):
        self._stop_flag = True

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        self.finalize()
