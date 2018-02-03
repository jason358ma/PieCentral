import flask
import threading
import time
import queue
from Utils import *
from LCM import *
from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room, send
import gevent
import json

LCM_URL = "192.0.0.1"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

RFID_list = '1|2|3|4|5|0'

@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)
    if message == 'generate-rfid':
        print('sending-rfid')
        lcm_send(LCM_TARGETS.SHEPHERD, SHEPHERD_HEADER.GENERATE_RFID)
        socketio.sleep(0.1)
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

    events = gevent.queue.Queue()
    lcm_start_read(str.encode(LCM_TARGETS.UI), events)
    counter = 0

    while True:
        print("help", counter)
        counter = (counter + 1) % 10;
        #RFID_list = str(counter) + RFID_list[1:]

        if (not events.empty()):
            event = events.get_nowait()
            print("RECEIVED:", event)
            if (event[0] == DAWN_HEADER.CALL_STATUS):
                socketio.emit(DAWN_HEADER.CALL_STATUS, json.dumps(event[1][0], ensure_ascii=False))
            elif (event[0] == DAWN_HEADER.CODE_LISTS):
                socketio.emit(DAWN_HEADER.CODE_LISTS, json.dumps(event[1][0], ensure_ascii=False))
        socketio.sleep(1)

socketio.start_background_task(receiver)
socketio.run(app)
