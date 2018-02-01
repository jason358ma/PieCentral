import flask
import threading
import time
from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room, send
import gevent

LCM_URL = "192.0.0.1"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

RFID_list = '1|2|3|4|5|0'

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/RFID_control.html/')
def RFID_control():
    return render_template('RFID_control.html')

@app.route('/score_adjustment.html/')
def score_adjustment():
    return render_template('score_adjustment.html')

@app.route('/staff_gui.html/')
def staff_gui():
    return render_template('staff_gui.html')

@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)
    if message == 'generate-rfid':
        print('sending-rfid')
        lcm_send(LCM_TARGETS.SHEPHERD, SHEPHERD_HEADER.GENERATE_RFID)
        socketio.sleep(2)
        socketio.emit('send-rfid', RFID_list)

@socketio.on('join')
def handle_join(client):
    print('confirmed join: ' + client)

@socketio.on('send')
def send_message(string):
    socketio.emit('send-rfid', string)
    print('Should have sent')

def receiver():
    global RFID_list

    events = queue.Queue()
    lcm_start_read(str.encode(LCM_TARGETS.UI), events)


    counter = 0
    while True:
        print("help", counter)
        counter = (counter + 1) % 10;
        RFID_list = str(counter) + RFID_list[1:]

        event = events.get(True)
        print("RECEIVED:", event)
        if (event[0] == 'help'):
            RFID_list = event[1][0]
        socketio.sleep(1)

socketio.start_background_task(receiver)
socketio.run(app)
