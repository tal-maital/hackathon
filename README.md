### Installation

```
sudo apt-get update
sudo apt-get install pigpio python-pigpio python3-pigpio
pip3 install adafruit-circuitpython-lsm6ds adafruit-circuitpython-lps2x adafruit-circuitpython-bno055 python-socketio eventlet flask-socketio gevent gevent-websocket picamera
sudo pigpiod
```

### Examples

```
from .drivers.lps2x.py import Barometer, BAROMETER_TYPE

barometer = Barometer(BAROMETER_TYPE.LPS22)

print(barometer.getPressure())
print(barometer.getTemperature())
```

```
from .drivers.altimu10v5 import Altimu10V5

sensor = Altimu10V5()

print(sensor.getData())

```
