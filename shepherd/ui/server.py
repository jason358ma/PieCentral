import flask
import threading
import time
from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room, send

LCM_URL = "192.0.0.1"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

RFID_list = '1|2|3|4|5|6'

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/RFID_control.html/')
def hello():
    return render_template('RFID_control.html')

@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)
    if message == 'generate-rfid':
        print('sending-rfid')
        socketio.emit('send-rfid', input('Input new RFID list'))

@socketio.on('join')
def handle_message(client):
    print('confirmed join: ' + client)

'''
exit = True
while exit:
    inputted = input('Enter 6 nums pipe separated')
    if inputted == 'exit':
        exit = False
    else:
        RFID_list = inputted
    gevent.sleep()'''
