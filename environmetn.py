# environment.py

import math

class Environment:
    def __init__(self, altitude=4000, sea_level_temp=288.15, sea_level_pressure=101325,
                 lapse_rate=0.0065, wind_horizontal=5.0, wind_direction=90.0, wind_vertical=0.5):
        self.altitude = altitude
        self.T0 = sea_level_temp
        self.P0 = sea_level_pressure
        self.lapse_rate = lapse_rate
        self.wind_horizontal = wind_horizontal
        self.wind_direction = wind_direction
        self.wind_vertical = wind_vertical

        self.g = 9.81
        self.R = 287.05

        self.temperature = self.compute_temperature()
        self.pressure = self.compute_pressure()
        self.density = self.compute_density()

    def compute_temperature(self):
        return self.T0 - self.lapse_rate * self.altitude

    def compute_pressure(self):
        exponent = self.g / (self.R * self.lapse_rate)
        return self.P0 * (1 - self.lapse_rate * self.altitude / self.T0) ** exponent

    def compute_density(self):
        return self.pressure / (self.R * self.temperature)

    def summary(self):
        print("=== ENVIRONMENTAL CONDITIONS ===")
        print(f"Altitude: {self.altitude} m")
        print(f"Temperature: {self.temperature:.2f} K")
        print(f"Pressure: {self.pressure:.2f} Pa")
        print(f"Air Density: {self.density:.3f} kg/m³")
        print(f"Wind (horizontal): {self.wind_horizontal} m/s (Direction: {self.wind_direction}°)")
        print(f"Wind (vertical): {self.wind_vertical} m/s")
