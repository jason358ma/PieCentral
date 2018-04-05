
# Running the server
In the command line:

    pip install flask-socketio
    pip install gevent
    export FLASK_APP=server.py
    flask run

Go to localhost:[PORTNUM]/[page_name.html] in a browser
# Server-side modifications

## Fill in a unique port number not used by another server or by local machine processes
Change the line:
```python
PORT = (NUM)
```

## Serving a new page with a jinja template
Add a new function with an @app.route decorator that returns render_template for a Jinja template:
```python
@app.route('/page.html/')
def page():
    return render_template('page.html')
```

## Receiving message from UI and forwarding it to LCM
Use the @socketio.on decorator to register an event handler to a specific callback:
```python
@socketio.on('ui-to-server-message-event-name')
def ui_to_server_message_name(received_data):
    lcm_send(LCM_TARGETS.SHEPHERD, SHEPHERD_HEADER.TARGET_NAME, json.loads(received_data))
```

## Inside the receiver loop sending a particular event to UI
Use socketio.emit to send an event name and some data:
```python
if event[0] == UI_HEADER.EVENT_NAME:
    socketio.emit('server-to-ui-message-event-name', json.dumps(event[1], ensure_ascii=False))
```

# Client-side JS modifications

Receiving a message from the server:
```javascript
socket.on('server-to-ui-message-event-name', function(data) {
    //do stuff
})
```

# Client-side HTML -> Jinja template modifications

Anywhere a static dependency is linked to, it must be replaced with a url_for() call:
```javascript
<script type="text/javascript" src="socket.io.js"></script>
```
becomes
```javascript
<script type="text/javascript" src={{url_for( 'static', filename='socket.io.js' )}}></script>
```
