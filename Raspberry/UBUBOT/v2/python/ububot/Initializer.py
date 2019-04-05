#!/usr/bin/python3
from ububot.Motor.MotorPair import MotorPair, MotorPairDirection, MotorIdentifier
from ububot.Motor.Servo import Servo, ServoGroup
from ububot.Sensor.IR import IRSensor
from ububot.Sensor.SensorGroup import CardinalGroup
from ububot.Relay.Relay import Relay
from ububot.Relay.RelayGroup import FunctionalGroup
from ububot.Comms.Socket import SocketCommunication
from ububot.Comms.Serial import SerialCommunication, SerialCapture

class UBUBOT(object):
    motors: MotorPair = None
    sensors: CardinalGroup = None
    relays: FunctionalGroup = None
    servos: ServoGroup = None
    serial: SerialCommunication = None
    socket: SocketCommunication = None
    serial_capture: SerialCapture = None
    _serial_captures = []

    def __init__(self, motors=False, sensors=False, relays=False, servos=False, serial=False, serial_capture=False, socket=False, motors_socket=False, serial_socket_capture=False, status_socket=False, all=False):
        status_listener = None
        if status_socket or all:
            status_listener = lambda status: self.socket.send_json("ububot-status", status)
        if socket or all or motors_socket or serial_socket_capture or status_socket:
            self.socket = SocketCommunication()
        if sensors or all:
            self.sensors = CardinalGroup(north=23, south=22, west=18, east=24, state_listener=status_listener)
        if relays or all:
            self.relays = FunctionalGroup(light=7, buzzer=13, motor_1=15, motor_2=11, state_listener=status_listener)
        if servos or all:
            servos_group = [Servo(channel, min_pwn=108, max_pwm=500, max_angle=120, state_listener=status_listener) for channel in range(8)]
            servos_group.extend([Servo(channel, min_pwn=200, max_pwm=2300, max_angle=360, state_listener=status_listener) for channel in range(8, 16)])
            self.servos = ServoGroup(servos_group)
        if serial or all or serial_capture or serial_socket_capture:
            self.serial = SerialCommunication()
        if serial_capture or all or serial_socket_capture:
            self.serial_capture = SerialCapture()
            self.serial_capture.start(lambda line: self._serial_capture_callback(line))
        if motors or all or motors_socket:
            if motors_socket or all:
                self.motors = MotorPair(lambda result: self.socket.send_json("ububot-function", result))
            else:
                self.motors = MotorPair()
        if serial_socket_capture or all:
            self.add_capture_callback(lambda line: self.socket.send("ububot-serial", line))
    
    def _serial_capture_callback(self, line):
        for callback in self._serial_captures:
            callback(line)
    
    def add_capture_callback(self, callback):
        self._serial_captures.append(callback)
    
    def clear_captures(self):
        self._serial_captures.clear()
    
    def pop_capture(self):
        self._serial_captures.pop()

    def finalize(self):
        if self.serial_capture:
            self.serial_capture.stop()
        if self.relays:
            Relay.clean_up()
        UBUBOT.disconnect_communications()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.finalize()
    
    @staticmethod
    def disconnect_communications():
        SocketCommunication.disconnect()
        SerialCommunication.disconnect()
