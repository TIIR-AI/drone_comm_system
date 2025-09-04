# server.py
from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt
import jwt
import datetime



# configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-very-secret-key' # CHANGE THIS IN PRODUCTION
socketio = SocketIO(app)

MQTT_BROKER = 'broker.emqx.io' # Using a public broker for this example
MQTT_PORT = 1883
DRONE_TOPIC = 'drone/123/telemetry'

# JWT Authentication
def generate_token(username):
    """Generates a JWT for a user."""
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        'iat': datetime.datetime.utcnow(),
        'sub': username
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

@app.route('/get-token/<username>')
def get_token(username):
    """Endpoint for the client to get a token."""
    token = generate_token(username)
    return jsonify({'token': token})

# MQTT Client Setup
def on_connect(client, userdata, flags, rc):
    """Callback for when the client connects to the broker."""
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(DRONE_TOPIC)
    else:
        print(f"Failed to connect, return code {rc}\n")

def on_message(client, userdata, msg):
    """Callback for when a message is received from the drone."""
    payload = msg.payload.decode()
    print(f"Received from drone: {payload}")
    # Broadcast the drone's data to all connected web clients
    socketio.emit('drone_update', payload)

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start() # Start a background thread to handle MQTT messages

# Web Server Routes
@app.route('/')
def index():
    ## Serves the main HTML page
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    ## Handles a new WebSocket connection from a user
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    ## Handles a WebSocket disconnection
    print('Client disconnected')

if __name__ == '__main__':
    # We use allow_unsafe_werkzeug for development purposes.
    # In a production environment, use a proper WSGI server like Gunicorn or uWSGI.
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)