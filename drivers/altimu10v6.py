import time
import board
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX

class Altimu10V6():
    def __init__(self):
        i2c = board.I2C() 
        self.accelerometer = LSM6DSOX(i2c)

    def calibrate(self):
        self.accelerometer.calibrate()

    def getData(self):
        return self.accelerometer.acceleration
