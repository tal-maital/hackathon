import pigpio

class Servo():
  def __init__(self, pin):
    self.pin = pin
    self.pigpio = pigpio.pi()
    self.pigpio.set_mode(pin, pigpio.OUTPUT)
  
  def __del__(self):
    self.pigpio.stop()

  def right(self):
    self.pigpio.set_servo_pulsewidth(self.pin, 2500)

  def left(self):
    self.pigpio.set_servo_pulsewidth(self.pin, 500)

  def stop(self):
    self.pigpio.set_servo_pulsewidth(self.pin, 0)