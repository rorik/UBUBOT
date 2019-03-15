#!/usr/bin/python3
from Motor.MotorPair import MotorPair, MotorPairDirection, MotorIdentifier
from Sensor.IR import IRSensor
from Sensor.SensorGroup import CardinalGroup
from Relay.Relay import Relay
from Relay.RelayGroup import FunctionalGroup
from Comms.Socket import SocketCommunication
from Comms.Serial import SerialCommunication, SerialCapture

class UBUBOT(object):
    motors = None
    sensors = None
    relays = None
    serial = None
    socket = None
    serial_capture = None
    _serial_captures = []

    def __init__(self, motors=False, sensors=False, relays=False, serial=False, serial_capture=False, socket=False, motors_socket=False, serial_socket_capture=False, all=False):
        if sensors or all:
            self.sensors = CardinalGroup(north=IRSensor(16), south=IRSensor(22), west=IRSensor(18), east=IRSensor(12))
        if relays or all:
            self.relays = FunctionalGroup(light=Relay(7), buzzer=Relay(11), motor_1=Relay(13), motor_2=Relay(15))
        if serial or all or serial_capture or serial_socket_capture:
            self.serial = SerialCommunication()
        if serial_capture or all or serial_socket_capture:
            self.serial_capture = SerialCapture()
            self.serial_capture.start(lambda line: self._serial_capture_callback(line))
        if socket or all or motors_socket or serial_socket_capture:
            self.socket = SocketCommunication()
        if motors or all or motors_socket:
            if motors_socket:
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
    
    @staticmethod
    def disconnect_communications():
        SocketCommunication.disconnect()
        SerialCommunication.disconnect()
