#!/usr/bin/python3
from ububot.Vision.CameraStream import CameraStream
from ububot.Vision.Line import get_stops, get_sections, get_paths
from ububot.Motor.MotorPair import MotorPair, MotorIdentifier
from threading import Thread, Timer, Event
from time import time
from math import sqrt, acos, pi


class LineFollower(Thread):
    def __init__(self, camera_stream: CameraStream, precision=20):
        super(LineFollower, self).__init__()
        if camera_stream is None:
            raise ValueError("Expected camera stream, but got None instead")
        self._camera_stream = camera_stream
        self._finalized = Event()
        self._queued = [Event(), None, tuple(), None]
        self.set_precision(precision)
    
    def run(self):
        while not self._finalized.isSet():
            self._queued[0].wait()
            if self._finalized.isSet():
                break
            self._queued[0].clear()
            if self._queued[1]:
                self._follow(self._queued[3], *self._queued[2])
            else:
                self._wait_for_stop(*self._queued[2])
    
    def set_precision(self, precision: int):
        self._precision = precision

    def wait_for_stop(self, min_y=-20, max_y=20, timeout=None, interrupt: Event = None):
        self._queued[1] = False
        self._queued[2] = (min_y, max_y, timeout, interrupt)
        self._queued[0].set()

    def _wait_for_stop(self, min_y=-20, max_y=20, timeout=None, interrupt: Event = None):
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
            
            stops = get_stops(get_sections(img, precision=self._precision))
            for relative_y, sections in stops.items():
                if min_y <= relative_y <= max_y and len(sections) > 0:
                    return True
    def follow(self, motors: MotorPair, speed=40, wait_for_stop=True, color_threshold=80, stop_threshold=30, min_y=-20, max_y=20, timeout=None, interrupt: Event = None, callback=None):
        self._queued[1] = True
        self._queued[2] = (speed, wait_for_stop, color_threshold, stop_threshold, min_y, max_y, timeout, interrupt, callback)
        self._queued[3] = motors
        self._queued[0].set()

    def _follow(self, motors: MotorPair, speed=40, wait_for_stop=True, color_threshold=80, stop_threshold=30, min_y=-20, max_y=20, timeout=None, interrupt: Event = None, callback=None):
        start = time() if timeout is not None else None
        previous_ratio = [None, None]
        while not self._finalized.is_set() and interrupt is None or not interrupt.is_set():
            # Calculate next timeout
            _timeout = None
            if start is not None:
                elapsed = time() - start
                if elapsed > timeout:
                    motors.stop()
                    return False
                _timeout = timeout - elapsed
            
            # Wait for image
            img = self._camera_stream.wait_for_capture(_timeout)
            if img is None:
                motors.stop()
                return False

            # Check stops
            sections = get_sections(img, threshold=color_threshold, precision=self._precision)
            stops = None
            if wait_for_stop:
                stops = get_stops(sections.copy(), threshold=stop_threshold)
                for relative_y, _sections in stops.items():
                    if min_y <= relative_y <= max_y and len(_sections) > 0:
                        motors.stop()
                        if callback is not None:
                            callback(img, sections, stops, None, None, None)
                        return True
            
            # Get path vector
            paths = get_paths(sections)
            longest_path = None
            vector = None
            if len(paths) > 0:
                longest_path = max(paths, key=len)
                if len(longest_path) > 1:
                    vector = self._convert_vector([longest_path[0], longest_path[-1]])
                    
                    # Apply speed reduction to each motor
                    ratio = [1, 1]
                    if vector[1] >= 0:
                        ratio[1] = 1 - vector[1] / 60
                    else:
                        ratio[0] = 1 + vector[1] / 60
                    
                    if ratio[0] != previous_ratio[0]:
                        previous_ratio[0] = ratio[0]
                        motors.run(MotorIdentifier.LEFT, speed*ratio[0])
                    
                    if ratio[1] != previous_ratio[1]:
                        previous_ratio[1] = ratio[1]
                        motors.run(MotorIdentifier.RIGHT, speed*ratio[1])

            if callback is not None:
                callback(img, sections, stops, paths, longest_path, vector)

    @staticmethod
    def _convert_vector(vector):
        h = vector[0][0] - vector[1][0]
        w = (vector[1][1][1] + vector[1][1][0] - vector[0][1][1] - vector[0][1][0]) / 2
        distance = sqrt(h * h + w * w)
        angle = acos((distance * distance + h * h - w * w) / (2 * distance * h)) * 180 / pi
        if w < 0:
            angle *= -1
        return (distance, angle)

    
    def finalize(self):
        self._finalized.set()
        self._queued[0].set()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        self.finalize()
        pass
