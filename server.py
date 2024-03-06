import socketio
import time
import eventlet

# create a Socket.IO server
sio = socketio.Server(cors_allowed_origins='*')

# create a WSGI application
app = socketio.WSGIApp(sio)

def send_status(parachute_armed, parachute_deployed):
    sio.emit('status', { 'parachuteArmed': parachute_armed, 'parachuteDeployed': parachute_deployed})

def send_rocket_data(altitude):
    sio.emit('rocket-data', { 'timestamp': time.time(), 'altitude': altitude})
    
# Event handler for new connections
@sio.event
def connect(sid, environ):
    print('connect ', sid)

# Event handler for messages
@sio.event
def message(sid, data):
    print('message ', data)
    sio.send(sid, f"Reply: {data}")

# Event handler for disconnections
@sio.event
def disconnect(sid):
    print('disconnect ', sid)

@sio.on('arm-parachute')
def arm_parachute(sid):
    print('arm-parachute')

    send_status(True, False)

@sio.on('disarm-parachute')
def arm_parachute(sid):
    print('disarm-parachute')

    send_status(False, False)

@sio.on('reset-parachute')
def arm_parachute(sid):
    print('reset-parachute')

    send_status(False, False)

@sio.on('deploy-parachute')
def arm_parachute(sid):
    print('deploy-parachute')

    send_status(True, True)

@sio.on('launch')
def arm_parachute(sid):
    print('launch')

def read_and_send_data():
    while True:
        send_rocket_data(1)
        eventlet.sleep(1) # Send data every 1 second


if __name__ == '__main__':
    eventlet.spawn(read_and_send_data)

    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)