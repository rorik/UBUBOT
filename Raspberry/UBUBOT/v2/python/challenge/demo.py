#!/usr/bin/python3
from ububot.Initializer import UBUBOT
from ububot.Vision.CameraStream import CameraStream
from ububot.Vision.Streamer import Streamer
from ububot.Sound.Player import Player, Sounds
from ububot.Motor.MotorPair import MotorIdentifier, MotorPairDirection
from ububot.Relay.RelayGroup import FunctionalIdentifier
from time import sleep


resolution=(640, 480)
framerate=12
socket_framerate=10
claw_channel=8
plow_channel=7

def change_light(ububot):
    ububot.relays.get_light().off()
    sleep(0.1)
    ububot.relays.get_light().on()


if __name__ == '__main__':
    with UBUBOT(all=True) as ububot, Player() as player:
        #CameraStream(resolution=resolution, framerate=framerate) as camera, \
        #Streamer(framerate=socket_framerate) as streamer, Player() as player:
        input("Press Enter to continue...")
        ububot.relays.get_buzzer().off()
        sleep(1)
        #camera.add_callback(streamer.set_image)
        player.play(Sounds.WIN_XP_ON)
        ububot.servos.get(plow_channel).angle(50)
        sleep(2)
        ububot.relays.get_buzzer().on()
        ububot.motors.advance_cm(40, speed=100)
        sleep(3)
        ububot.motors.turn_sharp(MotorPairDirection.SHARP_LEFT, speed=200, angle=180*4)
        sleep(2)
        ububot.motors.advance_cm(60, speed=100)
        sleep(4)
        change_light(ububot)
        ububot.motors.advance_cm(-10, speed=10)
        sleep(3)
        change_light(ububot)
        ububot.servos.get(claw_channel).angle(120)
        sleep(1)
        ububot.servos.get(claw_channel).angle(0)
        sleep(1)
        change_light(ububot)
        ububot.motors.move_by(MotorIdentifier.LEFT, speed=80, angle=600)
        ububot.motors.move_by(MotorIdentifier.RIGHT, speed=40, angle=300)
        sleep(4)
        ububot.servos.get(plow_channel).angle(70)
        sleep(1)
        ububot.servos.get(plow_channel).angle(50)
        ububot.servos.get(claw_channel).angle(0)
        sleep(1)
        change_light(ububot)
        sleep(0.1)
        change_light(ububot)
        ububot.motors.advance_cm(-30, speed=200)
        ububot.relays.get_buzzer().off()
        sleep(2)
        change_light(ububot)
        player.play(Sounds.SIREN)
        sleep(1)
        ububot.motors.turn_sharp(MotorPairDirection.SHARP_RIGHT, speed=100, angle=720*2.4)
        ububot.servos.get(plow_channel).angle(90)
        ububot.servos.get(claw_channel).angle(90)
        sleep(0.5)
        ububot.servos.get(plow_channel).angle(50)
        ububot.servos.get(claw_channel).angle(0)
        sleep(0.5)
        ububot.servos.get(plow_channel).angle(90)
        ububot.servos.get(claw_channel).angle(90)
        sleep(0.5)
        ububot.servos.get(plow_channel).angle(50)
        ububot.servos.get(claw_channel).angle(0)
        sleep(1)
        change_light(ububot)
        sleep(0.1)
        change_light(ububot)
        sleep(4)
        player.play(Sounds.WIN_XP_OFF)
        sleep(2)
        ububot.relays.get_buzzer().on()
        input("Press Enter to end...")


