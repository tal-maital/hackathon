from gpiozero import Servo

class PiServo():
  def __init__(self, pin):
    self.pin = pin
    self.servo = Servo(self.pin)
  
  def __del__(self):
    self.servo.value = None

  def right(self):
    self.servo.value = -1

  def left(self):
    self.servo.value = 1

  def stop(self):
    self.servo.value = None
