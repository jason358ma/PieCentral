
<h1>Running the server</h1>
<p>pip install flask-socketio</p>
<p>pip install gevent</p>
<p>export FLASK_APP=(server.py)</p>
<p>flask run</p>

<h1>Server-side modifications</h1>

<strong>Fill in a unique port number not used by another server or by local machine processes</strong>
<p>PORT = (NUM)</p>

<strong>Serving a new page with a jinja template</strong>
<p>@app.route('/page.html/')</p>
<p>def page():</p>
<p>    return render_template('page.html')</p>

<strong>Receiving message from UI and forwarding it to LCM</strong>
@socketio.on('ui-to-server-message-event-name')
def ui_to_server_message_name(received_data):
    lcm_send(LCM_TARGETS.SHEPHERD, SHEPHERD_HEADER.TARGET_NAME, json.loads(received_data))

<strong>Inside the receiver loop sending a particular event to UI</strong>
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
