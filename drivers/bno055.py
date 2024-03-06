import time
import board
import adafruit_bno055
from .imu import IMU

class BNO055():
    def __init__(self):
        i2c = board.I2C() 
        self.sensor = adafruit_bno055.BNO055_I2C(i2c)

    def getData(self):
        g_forces = self.sensor.acceleration
        angular_velocities = self.sensor.gyro  
        magnetometer_values = self.sensor.magnetic

        imu_data = IMU()
        imu_data.linear_acceleration_x = g_forces[0]
        imu_data.linear_acceleration_y = g_forces[1]
        imu_data.linear_acceleration_z = g_forces[2]
        imu_data.angular_velocity_x = angular_velocities[0]
        imu_data.angular_velocity_y = angular_velocities[1]
        imu_data.angular_velocity_z = angular_velocities[2]
        imu_data.magnetometer_x = magnetometer_values[0]
        imu_data.magnetometer_y = magnetometer_values[1]
        imu_data.magnetometer_z = magnetometer_values[2]
