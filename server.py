import csv
import time
import numpy as np
from datetime import datetime
import socketio
import gevent
from flask import Flask, Response
from flask_socketio import SocketIO
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from io import BytesIO
from camera_output import CameraOutput
from drivers.piservo import Servo
from drivers.camera import Camera

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*', async_mode='gevent')
servo = Servo

def write_headers(headers, file):
    with open(file, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)

def append_values(values, file):
    with open(file, mode='a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(values)

def calculate_altitude(pressure_hpa, temperature_c):
    # Constants
    temp_kelvin = temperature_c + 273.15  # Convert temperature to Kelvin
    sea_level_pressure = 1013.25  # Sea level standard atmospheric pressure in hPa
    gravitational_acceleration = 9.80665  # Acceleration due to gravity in m/s^2
    molar_mass_air = 0.0289644  # Molar mass of Earth's air in kg/mol
    universal_gas_constant = 8.3144598  # Universal gas constant in J/(mol*K)

    # Barometric formula
    altitude = ((universal_gas_constant * temp_kelvin) / (gravitational_acceleration * molar_mass_air)) \
        * np.log(sea_level_pressure / pressure_hpa) # In meters

    return altitude


def send_status(parachute_armed, parachute_deployed):
    socketio.emit('status', { 'parachuteArmed': parachute_armed, 'parachuteDeployed': parachute_deployed})

def send_rocket_data(altitude):
    socketio.emit('rocket-data', { 'timestamp': time.time(), 'altitude': altitude})
    
# Event handler for new connections
@socketio.event
def connect():
    print('Client connected')

# Event handler for messages
@socketio.event
def message(sid, data):
    print('message ', data)
    socketio.send(sid, f"Reply: {data}")

# Event handler for disconnections
@socketio.event
def disconnect():
    print('client disconnected')

@socketio.on('arm-parachute')
def arm_parachute():
    print('arm-parachute')

    send_status(True, False)

@socketio.on('disarm-parachute')
def arm_parachute():
    print('disarm-parachute')

    send_status(False, False)

@socketio.on('reset-parachute')
def arm_parachute():
    print('reset-parachute')

    send_status(False, False)

@socketio.on('deploy-parachute')
def arm_parachute():
    print('deploy-parachute')

    send_status(True, True)

@socketio.on('launch')
def arm_parachute():
    print('launch')

def record_video():
    camera = Picamera2()
    video_config = camera.create_video_configuration()
    camera.configure(video_config)
    encoder = H264Encoder(10000000)
    camera.start_recording(encoder, f'launch-{time.time()}.h264')

def generate_camera_stream(output):
    while True:
        with output.condition:
            output.condition.wait()
            frame = output.frame
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/stream')
def video_feed():
    return Response(generate_camera_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def read_and_send_data():
    while True:
        
        send_rocket_data(1)
        gevent.sleep(1) # Send data every 1 second, change this

if __name__ == '__main__':
    output = CameraOutput(f'video-{time.time()}.h264', 'mjpeg')
    datetime_str = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    log_filename = f'flight_logs_{datetime_str}.csv'
    log_headers = ["pressure", "total_accel",  ]

    write_headers(log_headers, log_filename)

    gevent.spawn(read_and_send_data)
    gevent.spawn(record_video)

    socketio.run(app, port=5000, host='0.0.0.0', debug=False)