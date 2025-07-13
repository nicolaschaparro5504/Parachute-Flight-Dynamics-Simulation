# File: /parachute-oscillation-estimator/parachute-oscillation-estimator/src/main.py

from flight_stages import FlightStages
from oscillation import OscillationEstimator
from utils.parameters import GRAVITY, AIR_DENSITY

def main():
    # Initialize flight parameters
    mass = 80  # kg
    drag_coefficient = 1.5
    area = 0.5  # m^2
    initial_height = 1000  # m
    max_time = 60  # s
    horizontal_speed = 1  # m/s

    # Create an instance of FlightStages
    flight = FlightStages(mass, drag_coefficient, area, initial_height, max_time, horizontal_speed=horizontal_speed)

    # Create an instance of OscillationEstimator
    oscillator = OscillationEstimator(flight)

    # Estimate angle of attack changes during descent
    angle_changes = oscillator.estimate_angle_of_attack()

    # Output the results
    for time, angle in angle_changes:
        print(f"Time: {time:.2f} s, Angle of Attack: {angle:.2f} degrees")

if __name__ == "__main__":
    main()