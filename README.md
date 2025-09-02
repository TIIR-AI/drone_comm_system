# drone_comm_system
secure drone communication system with GPS tracking


# Secure Drone Communication & Package Tracking System

This project implements a secure, real-time communication system for monitoring drone package deliveries. It features a ground control server, a simulated drone client, and a web-based user interface for live GPS tracking.


## Key Features

- **Real-Time GPS Tracking**: Monitor the drone's location live on an OpenStreetMap interface.
- **Secure Communication**: Uses the lightweight MQTT protocol for IoT communication and JWT for authenticating clients (in a full implementation).
- **Real-Time Status Updates**: Receive live updates from the drone, such as *"In Transit"* or *"Package Delivered"*.
- **Decoupled Architecture**: The drone and user client do not communicate directly; all messages are securely routed through the central server.
- **Simple Simulation**: Includes a script to simulate a drone flying a predefined path, making it easy to test the entire system.


## System Architecture

The system consists of three main components that communicate via an **MQTT message broker**:

- **Drone Client (`drone_client.py`)**  
  A Python script that simulates a drone. It periodically publishes its GPS coordinates and status updates to a specific MQTT topic.

- **Ground Control Server (`server.py`)**  
  A Flask server that subscribes to the MQTT topic. When it receives a message from the drone, it forwards the data to the user interface using WebSockets.

- **User Interface (`index.html`)**  
  A web page that connects to the server via WebSockets. It uses **Leaflet.js** to display the drone's location on a map and updates the status in real-time.

**Data Flow:**
Drone Client → MQTT Broker → Ground Control Server → User Interface (Web Browser)

## Technology Stack
- **Backend**: Python 3.10+, Flask, Flask-SocketIO  
- **Messaging Protocol**: MQTT (using `paho-mqtt` library)  
- **Frontend**: HTML, CSS, JavaScript, Leaflet.js, Socket.IO  
- **Security**: JSON Web Tokens (`PyJWT`) for authentication logic  

## Project Structure
```bash
drone_project/
├── templates/
│   └── index.html
├── .gitignore
├── drone_client.py
├── README.md
├── requirements.txt
└── server.py
```

## Setup and Installation
Clone the repo:
```
https://github.com/TIIR-AI/drone_comm_system.git
```

Create an env:
```
conda create -n "drone_comm_sys_test"
```

Install dependancies:
```
pip install -r requirements.txt
```

## Run 

You will need to open two seperate terminal windows.

In your first terminal, start the Flask server:
```
python server.py
```
 should see output indicating that the server is running and has connected to the MQTT broker.

 In your second terminal, run the drone simulation script:
 ```
 python drone_client.py
 ```

 This terminal will show log messages as the drone flies its path and publishes data.