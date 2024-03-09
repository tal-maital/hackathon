import board
from adafruit_lps2x import LPS22

class Lps22():
    def __init__(self):
        i2c = board.I2C()
        self.sensor = LPS22(i2c)

    def getPressure(self):
        return self.sensor.pressure

    def getTemperature(self):
        return self.sensor.temperature
