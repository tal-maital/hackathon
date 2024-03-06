
from dataclasses import dataclass

@dataclass
class IMU:
  linear_acceleration_x: float
  linear_acceleration_y: float
  linear_acceleration_z: float
  angular_velocity_x: float
  angular_velocity_y: float
  angular_velocity_z: float
  magnetometer_x: float
  magnetometer_y: float
  magnetometer_z: float
