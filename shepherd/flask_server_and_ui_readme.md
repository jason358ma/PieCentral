
# Running the server
In the command line:

    pip install flask-socketio
    pip install gevent
    export FLASK_APP=server.py
    flask run

Go to localhost://[PORTNUM]
# Server-side modifications

## Fill in a unique port number not used by another server or by local machine processes
Change the line:
```python
PORT = (NUM)
```

## Serving a new page with a jinja template
@app.route('/page.html/')

```python
def page():
    return render_template('page.html')
```

## Receiving message from UI and forwarding it to LCM
@socketio.on('ui-to-server-message-event-name')
def ui_to_server_message_name(received_data):
    lcm_send(LCM_TARGETS.SHEPHERD, SHEPHERD_HEADER.TARGET_NAME, json.loads(received_data))

## Inside the receiver loop sending a particular event to UI
if event[0] == UI_HEADER.EVENT_NAME:
    socketio.emit('server-to-ui-message-event-name', json.dumps(event[1], ensure_ascii=False))


Client-side JS modifications:

//Receiving a message from the server
socket.on('server-to-ui-message-event-name', function(data) {
    //do stuff
});

Client-side HTML template modifications:

<!--Anywhere a static dependency is linked to, it must be replaced with a url_for() call-->
<script type="text/javascript" src="socket.io.js"></script>
<!--becomes-->
<script type="text/javascript" src={{url_for( 'static', filename='socket.io.js' )}}></script>
