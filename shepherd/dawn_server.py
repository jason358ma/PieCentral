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
    lcm_start_read(str.encode(LCM_TARGETS.DAWN), events, json=True)
    counter = 0

    while True:
        if (not events.empty()):
            event = events.get_nowait()
            print("RECEIVED:", event)
            socketio.emit(DAWN_HEADER.CALL_STATUS, json.dumps(event[1], ensure_ascii=False))
        socketio.sleep(1)

socketio.start_background_task(receiver)
socketio.run(app, host=HOST_URL, port=PORT)
