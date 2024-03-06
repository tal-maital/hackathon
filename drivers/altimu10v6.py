import time
import board
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX
from .lis3mdl import LIS3MDL
from .imu import IMU

class Altimu10V6():
    def __init__(self):
        i2c = board.I2C() 
        self.accelerometer = LSM6DSOX(i2c)
        self.magnetometer = LIS3MDL()

        self.magnetometer.enable()

    def calibrate(self):
        self.accelerometer.calibrate()

    def getData(self):
        g_forces = self.accelerometer.acceleration
        angular_velocities = self.accelerometer.gyro
        magnetometer_values = self.magnetometer.get_magnetometer_raw()

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
