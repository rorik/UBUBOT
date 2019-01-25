#!/usr/bin/python3
from Motor.MotorPair import MotorPair, MotorPairDirection
from util.ConfigHelper import ConfigHelper
from util.angle import cartesian_to_polar
from Sensor.us_locker import USLocker
from steamcontroller import SteamController, SCButtons
from steamcontroller.events import EventMapper, Pos
from steamcontroller.daemon import Daemon
import gc
import argparse
import sys


def button_pressed_callback(evm, btn, pressed):
    if btn == SCButtons.STEAM:
        if not pressed:
            print("Exiting...")
            if lock is not None:
                lock.stop()
            sys.exit(0)
    elif btn == SCButtons.A:
        motors.lock()
        print("BYPASSED LOCK")


def touchpad_click_callback(evm, pad, pressed):
    if not pressed:
        motors.move(MotorPairDirection.STOP)
        print("Stopped")


def touchpad_touch_callback(evm, pad, x, y):
    speed, angle = cartesian_to_polar(x, y)
    motors.move(MotorPairDirection.POLAR, speed=speed, angle=angle)
    print("Applying Cartesian Direction ({}, {}) = (r={}, ϕ={:0.2f})".format(x, y, speed, angle))


def stick_pressed_callback(evm):
    print("Stick pressed")


def stick_axes_callback(evm, x, y):
    if x > 0:
        motors.reduce(right=x / 32768)
        print("Turning right by {:0.2f}%".format(x / 32768 * 100))
    elif x < 0:
        motors.reduce(left=x / -32768)
        print("Turning left by {:0.2f}%".format(- x / 32768 * 100))
    else:
        motors.reduce(left=0, right=0)
        print("Going straight")


def trigger_axes_callback(evm, pos, value):
    direction = 16 if pos == 0 else -16
    motors.straight(value * direction)
    print("Straight, speed =", (value + 1) * direction - 16 / direction)


def evminit():
    evm = EventMapper()
    evm.setButtonCallback(SCButtons.STEAM, button_pressed_callback)
    evm.setButtonCallback(SCButtons.A, button_pressed_callback)
    evm.setButtonCallback(SCButtons.B, button_pressed_callback)
    evm.setButtonCallback(SCButtons.X, button_pressed_callback)
    evm.setButtonCallback(SCButtons.Y, button_pressed_callback)
    evm.setButtonCallback(SCButtons.LB, button_pressed_callback)
    evm.setButtonCallback(SCButtons.RB, button_pressed_callback)
    evm.setButtonCallback(SCButtons.LT, button_pressed_callback)
    evm.setButtonCallback(SCButtons.RT, button_pressed_callback)
    evm.setButtonCallback(SCButtons.LGRIP, button_pressed_callback)
    evm.setButtonCallback(SCButtons.RGRIP, button_pressed_callback)
    evm.setButtonCallback(SCButtons.START, button_pressed_callback)
    evm.setButtonCallback(SCButtons.BACK, button_pressed_callback)
    evm.setPadButtonCallback(Pos.LEFT, touchpad_touch_callback)
    evm.setPadButtonCallback(Pos.RIGHT, touchpad_click_callback, clicked=True)
    evm.setStickAxesCallback(stick_axes_callback)
    evm.setStickPressedCallback(stick_pressed_callback)
    evm.setTrigAxesCallback(Pos.RIGHT, trigger_axes_callback)
    evm.setTrigAxesCallback(Pos.LEFT, trigger_axes_callback)
    return evm


class SCDaemon(Daemon):
    def __init__(self, pidfile, locker=None):
        super().__init__(pidfile)
        self.lock = locker

    def set_lock(self, locker):
        self.lock = locker

    def run(self):
        if self.lock is not None:
            self.lock.start()
        dm_evm = evminit()
        dm_sc = SteamController(callback=dm_evm.process)
        dm_sc.run()
        del dm_sc
        del dm_evm
        gc.collect()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', type=str, choices=['start', 'stop', 'restart', 'run'])
    parser.add_argument('-i', '--index', type=int, choices=[0, 1, 2, 3], default=None)
    parser.add_argument('-c', '--config', type=str, default="/etc/cb/UBUBOT/config")
    parser.add_argument('-v', action='store_true')
    args = parser.parse_args()

    config = ConfigHelper.load_config(args.config)
    motors = MotorPair(config)

    if args.index is None:
        daemon = SCDaemon('/tmp/steamcontroller.pid')
    else:
        daemon = SCDaemon('/tmp/steamcontroller{:d}.pid'.format(args.index))
    print("A")
    lock = None
    if config.UltraSonicLock:
        if config.UltraSonicMode != 4:
            lock = USLocker(config, motors)
        # else:
            # TODO: Interruption Lock
        daemon.set_lock(lock)
    print("B")

    if config.Handshake:
        ConfigHelper.handshake(config)
    print("C")

    if args.command == 'start':
        daemon.start()
    elif args.command == 'stop':
        daemon.stop()
    elif args.command == 'restart':
        daemon.restart()
    elif args.command == 'run':
        if lock is not None:
            lock.verbose = args.v
            lock.start()
        sc = SteamController(callback=evminit().process)
        sc.run()
    print("D")
