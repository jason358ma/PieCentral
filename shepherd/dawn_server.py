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

HOST_URL = "127.0.0.1"
PORT = 7000

app = Flask(__name__)
app.config['SECRET_KEY'] = 'omegalul!'
socketio = SocketIO(app)

def receiver():
    events = gevent.queue.Queue()
    lcm_start_read(str.encode(LCM_TARGETS.DAWN), events)
    counter = 0

    while True:
        print("help", counter)
        counter = (counter + 1) % 10;
        #RFID_list = str(counter) + RFID_list[1:]

        if (not events.empty()):
            event = events.get_nowait()
            print("RECEIVED:", event)
            if (event[0] == DAWN_HEADER.CALL_STATUS):
                socketio.emit(DAWN_HEADER.CALL_STATUS, event[1][0])
            elif (event[0] == DAWN_HEADER.CODE_LISTS):
                socketio.emit(DAWN_HEADER.CODE_LISTS, event[1][0])
        socketio.sleep(1)

socketio.start_background_task(receiver)
socketio.run(app, host=HOST_URL, port=PORT)
