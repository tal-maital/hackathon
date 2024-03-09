import numpy as np
from datetime import datetime
import time
import csv
from drivers.lps22 import Lps22
from drivers.altimu10v6 import Altimu10V6

def calculate_altitude(pressure_hpa, temperature_c):
    # Constants
    temp_kelvin = temperature_c + 273.15  # Convert temperature to Kelvin
    sea_level_pressure = 1013.25  # Sea level standard atmospheric pressure in hPa
    gravitational_acceleration = 9.80665  # Acceleration due to gravity in m/s^2
    molar_mass_air = 0.0289644  # Molar mass of Earth's air in kg/mol
    universal_gas_constant = 8.3144598  # Universal gas constant in J/(mol*K)

    # Barometric formula
    altitude = ((universal_gas_constant * temp_kelvin) / (gravitational_acceleration * molar_mass_air)) \
        * np.log(sea_level_pressure / pressure_hpa) # In meters

    return altitude

def write_headers(headers, file):
    with open(file, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)

def append_values(values, file):
    with open(file, mode='a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(values)

def main():
    log_filename = f'flight_logs_{datetime.now().strftime("%Y-%m-%d-%H%M%S")}.csv'
    log_headers = ["timestamp", "accel-x", "accel-y", "accel-z", "pressure", "temperature", "altitude"]
    write_headers(log_headers, log_filename)
    
    altimu = Altimu10V6()  # Init Altimu10V6
    barometer = Lps22() # Init Lps22

    while True:
        pressure = barometer.getPressure()
        temp = barometer.getTemperature()
        altitude = calculate_altitude(pressure, temp) #- init_altitude
        accel = altimu.getData()  # Get the acceleration data
        print(f"P: {pressure}, T: {temp}, Altitude: {altitude}, Accel: X={accel[0]}g, Y={accel[1]}g, Z={accel[2]}g    ", end = "\r>
        append_values([time.time() ,acceleration[0], acceleration[1], acceleration[2]], log_filename)
        time.sleep(1)  # Sleep for a second to limit the rate of data fetching

if __name__ == "__main__":
    main()

