import time
import board
import adafruit_lps2x
from enum import Enum

class BAROMETER_TYPE(Enum):
    LPS22 = 0,
    LPS25 = 1

class Barometer():
    def __init__(self, bar_type):
        i2c = board.I2C(1) 
        
        if bar_type == BAROMETER_TYPE.LPS22:
            self.lps = adafruit_lps2x.LPS22(i2c)
        elif bar_type == BAROMETER_TYPE.LPS25:
            self.lps = adafruit_lps2x.LPS22(i2c)

        raise Exception(f"Unknown barometer type: {bar_type}")
        
    def getPressure(self):
        return self.lps.pressure
    
    def getTemperature(self):
        return self.lps.temperature