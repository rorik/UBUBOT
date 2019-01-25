#!/usr/bin/python3
# import threading
import threading
import smbus
import time

from Motor.Motor import MotorDirection

DEVICE_ADDRESS = 0x10
STATUS_CMD = 20


class MyThread(threading.Thread):
    def __init__(self, event, runnable, delay):
        super().__init__()
        self.stopped = event
        self.delay = delay
        self.runnable = runnable

    def run(self):
        while not self.stopped.wait(self.delay):
            self.runnable()


class USLocker(object):
    def verify_position(self):
        lock = MotorDirection.STOP
        lock_cause = None
        if self.mode == 3:
            try:
                status = self.get(STATUS_CMD + self.distance)
                if status & 127 != 127:
                    status &= 7
                    for i in range(3):
                        if (status & 1 << i) > 0:
                            lock = self.direction
                            lock_cause = i
                            break
            except OSError:
                pass

        else:
            for i in range(3):
                try:
                    if self.check_distance(i):
                        lock = self.direction
                        lock_cause = i
                        break
                except OSError:
                    pass
        if self.locked != (lock == self.direction):
            if self.verbose:
                if lock == self.direction:
                    print("Direction", self.direction, "locked due to sensor", lock_cause)
                else:
                    print("Direction", self.direction, "unlocked")
            self.locked = not self.locked
        self.motors.lock(lock)
        time.sleep(self.delay)

    def check_distance(self, sensor):
            return self.get(sensor + 127 * self.mode) <= self.distance

    def get(self, request):
        return self.bus.read_byte_data(DEVICE_ADDRESS, request)

    def __init__(self, config, motors, direction=MotorDirection.FORWARDS, verbose=False):
        self.bus = smbus.SMBus(config.I2CBus)
        self.distance = config.UltraSonicThreshold
        self.delay = config.UltraSonicPollingDelay / 1000
        self.motors = motors
        self.mode = config.UltraSonicMode
        self.direction = direction
        self.verbose = verbose
        self.stopFlag = threading.Event()
        self.locked = False
        self.thread = MyThread(self.stopFlag, self.verify_position, 1 / config.UltraSonicPollingRate)

    def start(self):
        if self.verbose:
            print("Lock started")
        self.thread.start()

    def stop(self):
        self.stopFlag.set()
        if self.verbose:
            print("Lock stopped")
