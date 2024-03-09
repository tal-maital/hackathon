import os
import csv
import time
import numpy as np
from datetime import datetime
import socketio
import gevent
from flask import Flask, send_from_directory
from flask_socketio import SocketIO
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from drivers.piservo import PiServo
from drivers.lps22 import Lps22
from drivers.altimu10v6 import Altimu10V6

app = Flask(__name__, static_folder='fe', static_url_path='')
socketio = SocketIO(app, cors_allowed_origins='*', async_mode='gevent')

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

def record_video(filename):
    video_config = camera.create_video_configuration()
    camera.configure(video_config)
    encoder = H264Encoder(10000000)
    camera.start_recording(encoder, filename)

def stop_video():
    camera.stop_recording()

def read_and_send_data(log_filename):
    while True:
        timestamp = time.time()
        acceleration = altimu.getData()
        pressure = barometer.getPressure()
        temperature = barometer.getTemperature()
        altitude = calculate_altitude(pressure, temperature)

        append_values([timestamp, acceleration[0], acceleration[1], acceleration[2], pressure, 
                       temperature, altitude], log_filename)
        
        send_rocket_data(altitude)

        gevent.sleep(0.02) # Send data every 0.02 seconds

def wait_and_deploy_parachute():
    previous_altitude = None

    while True:
        pressure = barometer.getPressure()
        temperature = barometer.getTemperature()
        altitude = calculate_altitude(pressure, temperature)
        altitude_delta = altitude - previous_altitude if previous_altitude else 0

        if altitude_delta < -2: 
            print(f"{altitude_delta} => moving servo...")
            servo.right()

        gevent.sleep(2) # Send data every 0.02 seconds
        previous_altitude = altitude


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
def disarm_parachute():
    print('disarm-parachute')
    send_status(False, False)

@socketio.on('reset-parachute')
def reset_parachute():
    print('reset-parachute')
    send_status(False, False)

@socketio.on('deploy-parachute')
def deploy_parachute():
    print('deploy-parachute')
    send_status(True, True)

@socketio.on('launch')
def launch():
    print('launch')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    camera = Picamera2() # Init Camera
    servo = PiServo(13) # Init Servo
    altimu = Altimu10V6()  # Init IMU
    barometer = Lps22() # Init Barometer

    datetime_str = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    log_headers = ["timestamp", "acc-x", "acc-y", "acc-z", "pressure", "temperature", "altitude"]
    log_filename = f'flight_logs_{datetime_str}.csv'
    video_filename = f'flight_video_{datetime_str}.mp4'

    write_headers(log_headers, log_filename)

    gevent.spawn(read_and_send_data, log_filename)
    gevent.spawn(record_video, video_filename)
    gevent.spawn(wait_and_deploy_parachute)

    current_directory = os.path.dirname(os.path.abspath(__file__))
    ssl_cert_path = os.path.join(current_directory, 'certificate.crt')
    ssl_key_path = os.path.join(current_directory, 'private.key')
    socketio.run(app, port=5000, host='0.0.0.0', debug=False, certfile=ssl_cert_path, keyfile=ssl_key_path)
