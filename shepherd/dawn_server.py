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

HOST_URL = "0.0.0.0"
PORT = 7000

app = Flask(__name__)
app.config['SECRET_KEY'] = 'omegalul!'
socketio = SocketIO(app)

def receiver():
    events = gevent.queue.Queue()
    lcm_start_read(str.encode(LCM_TARGETS.DAWN), events, put_json=True)
    counter = 0

    while True:
        if (not events.empty()):
            event = events.get_nowait()
            eventDict = json.loads(event)
            print("RECEIVED:", event)
            if eventDict["header"] == DAWN_HEADER.ROBOT_STATE:
                socketio.emit(DAWN_HEADER.ROBOT_STATE, event)
            else: 
                socketio.emit(DAWN_HEADER.CODES, event)
        socketio.emit(DAWN_HEADER.HEARTBEAT, json.dumps({"heartbeat" : 1}))
        socketio.sleep(1)

socketio.start_background_task(receiver)
socketio.run(app, host=HOST_URL, port=PORT)
