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
PORT = 5000

app = Flask(__name__)
app.config['SECRET_KEY'] = 'omegalul!'
socketio = SocketIO(app)

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

@socketio.on('join')
def handle_join(client_name):
    print('confirmed join: ' + client_name)

'''@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)
    if message == 'generate-rfid':
        print('sending-rfid')
        lcm_send(LCM_TARGETS.SHEPHERD, SHEPHERD_HEADER.GENERATE_RFID)
        socketio.sleep(0.1)'''

#Score Adjustment
@socketio.on('ui-to-server-scores')
def ui-to-server-scores(scores):
    lcm_send(LCM_TARGETS.SHEPHERD, SHEPHERD_HEADER.SCORE_ADJUST, json.loads(scores))

@socketio.on('ui-to-server-score-request')
def ui-to-server-score-request():
    lcm_send(LCM_TARGETS.SHEPHERD, SHEPHERD_HEADER.GET_SCORES)

#RFID_control
@socketio.on('ui-to-server-rfid-request')
def ui-to-server-rfid-request():
    lcm_send(LCM_TARGETS.SHEPHERD, SHEPHERD_HEADER.GENERATE_RFID)

#Main GUI
@socketio.on('ui-to-server-teams-info-request')
def ui-to-server-ui-request():
    lcm_send(LCM_TARGETS.SHEPHERD, SHEPHERD_HEADER.GET_MATCH_INFO)

@socketio.on('ui-to-server-setup-match')
def ui-to-server-ui-request(teams_info):
    lcm_send(LCM_TARGETS.SHEPHERD, SHEPHERD_HEADER.GET_MATCH_INFO, json.loads(teams_info))

@socketio.on('ui-to-server-start-match')
def ui-to-server-ui-request():
    lcm_send(LCM_TARGETS.SHEPHERD, SHEPHERD_HEADER.START_MATCH)

@socketio.on('ui-to-server-start-next-stage')
def ui-to-server-ui-request():
    lcm_send(LCM_TARGETS.SHEPHERD, SHEPHERD_HEADER.START_NEXT_STAGE)

@socketio.on('ui-to-server-reset-stage')
def ui-to-server-ui-request():
    lcm_send(LCM_TARGETS.SHEPHERD, SHEPHERD_HEADER.RESET_CURRENT_STAGE)

@socketio.on('ui-to-server-reset-match')
def ui-to-server-ui-request():
    lcm_send(LCM_TARGETS.SHEPHERD, SHEPHERD_HEADER.RESET_MATCH)

'''
E-stop is not implemented
@socketio.on('ui-to-server-stop-robot')
def ui-to-server-ui-request(json):
    lcm_send(LCM_TARGETS.SHEPHERD, SHEPHERD_HEADER.STOP_ROBOT, json.loads(scores))
'''

def receiver():
    events = gevent.queue.Queue()
    lcm_start_read(str.encode(LCM_TARGETS.UI), events)
    counter = 0

    while True:
        print("help", counter)
        counter = (counter + 1) % 10;

        if (not events.empty()):
            event = events.get_nowait()
            print("RECEIVED:", event)
            if (event[0] == UI_HEADER.RFID_LIST):
                socketio.emit('server-to-ui-rfidlist', json.dumps(event[1], ensure_ascii=False))
            elif (event[0] == UI_HEADER.TEAMS_INFO):
                socketio.emit('server-to-ui-teamsinfo', json.dumps(event[1], ensure_ascii=False))
            elif (event[0] == UI_HEADER.SCORES):
                socketio.emit('server-to-ui-scores', json.dumps(event[1], ensure_ascii=False))
        socketio.sleep(1)

socketio.start_background_task(receiver)
socketio.run(app, host=HOST_URL, port=PORT)
