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
PORT = 6000

app = Flask(__name__)
app.config['SECRET_KEY'] = 'omegalul!'
socketio = SocketIO(app)

def receiver():

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
            if (event[0] == SCOREBOARD_HEADER.SCORE):
                socketio.emit(SCOREBOARD_HEADER.SCORE, json.dumps(event[1][0], ensure_ascii=False))
            elif (event[0] == SCOREBOARD_HEADER.TEAMS):
                socketio.emit(SCOREBOARD_HEADER.TEAMS, json.dumps(event[1][0], ensure_ascii=False))
            elif (event[0] == SCOREBOARD_HEADER.BID_TIMER_START):
                socketio.emit(SCOREBOARD_HEADER.BID_TIMER_START, json.dumps(event[1][0], ensure_ascii=False))
            elif (event[0] == SCOREBOARD_HEADER.BID_AMOUNT):
                socketio.emit(SCOREBOARD_HEADER.BID_AMOUNT, json.dumps(event[1][0], ensure_ascii=False))
            elif (event[0] == SCOREBOARD_HEADER.BID_WIN):
                socketio.emit(SCOREBOARD_HEADER.BID_WIN, json.dumps(event[1][0], ensure_ascii=False))
            elif (event[0] == SCOREBOARD_HEADER.STAGE):
                socketio.emit(SCOREBOARD_HEADER.STAGE, json.dumps(event[1][0], ensure_ascii=False))
            elif (event[0] == SCOREBOARD_HEADER.STAGE_TIMER_START):
                socketio.emit(SCOREBOARD_HEADER.STAGE_TIMER_START, json.dumps(event[1][0], ensure_ascii=False))
            elif (event[0] == SCOREBOARD_HEADER.POWERUPS):
                socketio.emit(SCOREBOARD_HEADER.POWERUPS, json.dumps(event[1][0], ensure_ascii=False))
            elif (event[0] == SCOREBOARD_HEADER.ALLIANCE_MULTIPLIER):
                socketio.emit(SCOREBOARD_HEADER.ALLIANCE_MULTIPLIER, json.dumps(event[1][0], ensure_ascii=False))

        socketio.sleep(1)

socketio.start_background_task(receiver)
socketio.run(app, host=HOST_URL, port=PORT)
