#!/usr/bin/python3
import socketio
import json
import atexit


class SocketCommunication:
    _connection = None

    def __init__(self):
        if SocketCommunication._connection is None:
            SocketCommunication._connection = socketio.Client()
            SocketCommunication._connection.connect('http://localhost:80')
            atexit.register(SocketCommunication.disconnect)

    def send(self, label, data):
        if SocketCommunication._connection is not None:
            SocketCommunication._connection.emit(label, data)

    def send_json(self, label, data):
        self.send(label, json.dumps(data))

    @staticmethod
    def disconnect():
        if SocketCommunication._connection is not None:
            SocketCommunication._connection.disconnect()
            SocketCommunication._connection = None
