from parachute import Parachute
from Payload import Payload
from environment import Environment
from flight_stages import FlightStages
from Oscillations import ParachuteOscillationEstimator
from Forcecalculator import ForcesCalculator

def get_float(prompt, default):
    try:
        return float(input(f"{prompt} [default: {default}]: ") or default)
    except ValueError:
        print("Invalid input. Using default value.")
        return default

def get_str(prompt, default):
    return input(f"{prompt} [default: {default}]: ") or default

def main():
    print("=== PARACHUTE DESCENT SIMULATION ===")

    # Payload input
    payload_mass = get_float("Enter payload mass (kg)", 12.0)
    payload_shape = get_str("Enter payload shape (cuboid/cylinder/sphere)", "cuboid")
    payload_width = get_float("Enter payload width (m)", 0.2)
    payload_height = get_float("Enter payload height (m)", 0.2)
    payload_depth = get_float("Enter payload depth (m)", 0.2)
    payload = Payload("UserPayload", payload_mass, payload_shape, payload_width, payload_height, payload_depth)

    # Parachute input
    parachute_diameter = get_float("Enter parachute diameter (m)", 10.0)
    parachute_cd = get_float("Enter parachute drag coefficient", 1.5)
    parachute_shape = get_str("Enter parachute shape", "reefed")
    parachute_mass = get_float("Enter parachute mass (kg)", 5.0)
    parachute = Parachute(parachute_diameter, parachute_cd, shape=parachute_shape, mass=parachute_mass)
    parachute.plot_inflation_profile()  # Plot inflation profile
    parachute.print_area()  # Print drag area

    # Environment input
    altitude = get_float("Enter deployment altitude (m)", 1000)
    wind_horizontal = get_float("Enter horizontal wind speed (m/s)", 1.0)
    environment = Environment(altitude=altitude, wind_horizontal=wind_horizontal)
    environment.summary()  # Print environmental conditions


    # Flight simulation
    flight = FlightStages(
        payload=payload,
        parachute=parachute,
        environment=environment,
        t_max=60,
        t_deploy= 2,
        horizontal_speed=wind_horizontal
    )

    flight.simulate()  # Show trajectory, velocity, acceleration
    print(f"\nTerminal Velocity: {flight.terminal_velocity():.3f} m/s")

    # Oscillation analysis
    estimator = ParachuteOscillationEstimator(
        parachute=parachute,
        flight_stages=flight,
        damping_ratio=0.15,
        natural_freq=0.8,
        initial_angle=5.0
    )
    estimator.plot_oscillations()

    # Forces calculation
    forces_calculator = ForcesCalculator(environment, payload, parachute)

    reports = [payload, parachute, forces_calculator]
    for obj in reports:
        obj.report()
        
def is_fully_inflated(parachute, time):
    """
    Check if the parachute is fully inflated at a given time.
    """
    return parachute.is_fully_inflated(time)

if __name__ == "__main__":
    main()
