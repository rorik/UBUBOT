#!/usr/bin/python3
from Comms.Socket import SocketCommunication
import cv2
import base64
import threading

class Streamer(threading.Thread):
    def __init__(self, interval=1.0):
        super(Streamer, self).__init__()
        self.socket = SocketCommunication()
        self.stop_flag = False
        self.image = None
        self.interval = interval

    def run(self):
        if not self.stop_flag:
            threading.Timer(self.interval, self.run).start()
            if self.image is not None:
                self.socket.send_json('ububot-img', {"src": base64.b64encode(cv2.imencode('.jpg', self.image)[1]).decode('utf-8')})

    def set_image(self, image):
        self.image = image
    
    def finalize(self):
        self.stop_flag = True
        self.socket.disconnect()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        self.finalize()
