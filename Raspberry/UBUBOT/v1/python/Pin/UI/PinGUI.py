from flask import Flask
from flask import render_template
from Pin.Pin import Pin

app = Flask(__name__, static_url_path='/static')
pin = [Pin(9)] * 1


class PinInterface(object):
    def __init__(self, pins, port=80):
        start_server(pins, port)


def start_server(pins, port):
    global pin
    pin = pins
    print(pin)
    app.run(port=port)


@app.route('/')
def hello_world():
    return render_template('gpiogui.html')


@app.route('/read/pin/<int:num>')
def gpio_read(num):
    if num in range(1, len(pin) + 1):
        return str(pin[num - 1].name)
    else:
        return 'ERROR: UNKNOWN PIN { ' + str(num) + ' }'
