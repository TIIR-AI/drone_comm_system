# drone_client.py
import paho.mqtt.client as mqtt
import time
import json
import random

# --- Configuration ---
MQTT_BROKER = 'broker.emqx.io'
MQTT_PORT = 1883
DRONE_ID = '123'
DRONE_TOPIC = f'drone/{DRONE_ID}/telemetry'
FLIGHT_PATH_FILE = 'flight_path.json'

# --- Function to load the flight path from a JSON file ---
def load_flight_path(file_path):
    """Loads the flight path from a specified JSON file."""
    try:
        with open(file_path, 'r') as f:
            path = json.load(f)
            print(f"Successfully loaded flight path from {file_path}")
            return path
    except FileNotFoundError:
        print(f"ERROR: Flight path file not found at {file_path}. Exiting.")
        return None
    except json.JSONDecodeError:
        print(f"ERROR: Could not decode JSON from {file_path}. Check for syntax errors.")
        return None

def on_connect(client, userdata, flags, rc):
    """Callback for MQTT connection."""
    if rc == 0:
        print("Drone client connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}\n")

# --- Main Simulation Logic ---
flight_path = load_flight_path(FLIGHT_PATH_FILE)

if flight_path:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    client.on_connect = on_connect
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()

    print("Starting drone simulation...")

    try:
        for point in flight_path:
            # Add a little randomness to the coordinates
            lat = point['lat'] + random.uniform(-0.0001, 0.0001)
            lon = point['lon'] + random.uniform(-0.0001, 0.0001)
            
            payload = json.dumps({
                "drone_id": DRONE_ID,
                "location": {"lat": lat, "lon": lon},
                "status": point['status'],
                "timestamp": time.time()
            })
            
            result = client.publish(DRONE_TOPIC, payload)
            status = result[0]
            if status == 0:
                print(f"Sent `{payload}` to topic `{DRONE_TOPIC}`")
            else:
                print(f"Failed to send message to topic {DRONE_TOPIC}")
                
            time.sleep(2) # Wait 5 seconds before sending the next update

    except KeyboardInterrupt:
        print("Simulation stopped.")
    finally:
        client.loop_stop()
        client.disconnect()