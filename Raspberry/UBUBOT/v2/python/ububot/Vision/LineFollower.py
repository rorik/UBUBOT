#!/usr/bin/python3
from ububot.Vision.CameraStream import CameraStream
from ububot.Vision.Line import get_stops, get_sections, get_paths
from ububot.Motor.MotorPair import MotorPair
from threading import Thread, Timer, Event
from picamera.array import PiRGBArray
from picamera import PiCamera
from time import time


class LineFollower(Thread):
    def __init__(self, camera_stream: CameraStream, precision=20):
        super(LineFollower, self).__init__()
        if camera_stream is None:
            raise ValueError("Expected camera stream, but got None instead")
        self._camera_stream = camera_stream
        self._finalized = Event()
        self.set_precision(precision)
    
    def set_precision(self, precision: int):
        self._precision = precision

    def wait_for_stop(self, min_y=-20, max_y=20, timeout=None, interrupt: Event = None):
        start = time() if timeout is not None else None
        while not self._finalized.is_set() and interrupt is None or not interrupt.is_set():
            _timeout = None
            if start is not None:
                elapsed = time() - start
                if elapsed > timeout:
                    return False
                _timeout = timeout - elapsed

            img = self._camera_stream.wait_for_capture(_timeout)
            if img is None:
                return False
            
            stops = get_stops(get_sections(img, self._precision))
            for relative_y, sections in stops.items():
                if min_y <= relative_y <= max_y and len(sections) > 0:
                    return True
    
    def follow(self, motors: MotorPair, wait_for_stop=True, min_y=-20, max_y=20, timeout=None, interrupt: Event = None):
        start = time() if timeout is not None else None
        while not self._finalized.is_set() and interrupt is None or not interrupt.is_set():
            # Calculate next timeout
            _timeout = None
            if start is not None:
                elapsed = time() - start
                if elapsed > timeout:
                    return False
                _timeout = timeout - elapsed
            
            # Wait for image
            img = self._camera_stream.wait_for_capture(_timeout)
            if img is None:
                return False

            # Check stops
            sections = get_sections(img, self._precision)
            if wait_for_stop:
                stops = get_stops(sections)
                for relative_y, sections in stops.items():
                    if min_y <= relative_y <= max_y and len(sections) > 0:
                        return True
            
            # Check paths
            paths = get_paths(sections)
            longest_path = max(paths, key=len)
            vector = [longest_path[0], longest_path[-1]]
            print(longest_path)
            print(vector)
            print('----')

    
    def finalize(self):
        self._finalized.set()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        self.finalize()
        pass
