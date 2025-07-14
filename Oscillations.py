import math
import numpy as np
import matplotlib.pyplot as plt
from parachute import Parachute
from flight_stages import FlightStages
from Payload import Payload
from environmetn import Environment

cubesat = Payload("CubeSat-Alpha", 12.0, "cuboid", 0.2, 0.2, 0.2)
p1 = Parachute(10, 1.5, mass=5, shape="reefed")
env = Environment(altitude=1000)

td = FlightStages(
    payload=cubesat,
    parachute=p1,
    environment=env,
    t_max=60,
    t_deploy=2.0,
    horizontal_speed=1.0
)

class ParachuteOscillationEstimator:
    def __init__(self, parachute: Parachute, flight_stages: FlightStages, damping_ratio=0.15, natural_freq=0.8, initial_angle=5.0, z0=1000, t_max=60):
        """
        Estimate angle of attack oscillations during descent using parachute parameters.
        """
        self.flight_stages = flight_stages
        self.parachute = parachute
        # Use total mass from flight_stages for initial calculation
        self.mass = flight_stages.total_mass
        self.zeta = damping_ratio  # Damping ratio (ζ)
        self.omega_n = natural_freq  # Natural frequency (ω_n) [rad/s]
        self.theta0 = np.deg2rad(initial_angle)  # Initial angle of attack [rad]
        self.z0 = flight_stages.z0  # Initial altitude [m]
        self.t_max = flight_stages.t_max  # Maximum simulation time [s]
        self.terminal_velocity = flight_stages.terminal_velocity()  # Terminal descent velocity [m/s]

        # Update with parachute's actual mass and drag area
        self.mass = parachute.mass
        self.drag_area = self.parachute.drag_area

    def simulate(self, dt=0.1):
        """
        Simulate oscillations and descent.

        Angle of attack oscillations are modeled as a damped harmonic oscillator:
            θ(t) = θ₀ · exp(-ζ·ωₙ·t) · cos(ω_d·t)
        where:
            θ₀ = initial angle [rad]
            ζ = damping ratio
            ωₙ = natural frequency [rad/s]
            ω_d = damped natural frequency = ωₙ·sqrt(1 - ζ²)

        Altitude is modeled as a uniform descent at terminal velocity:
            z(t) = z₀ - v_terminal · t
        """
        t, z, _, _, _ = self.flight_stages.generate_trajectory(dt=dt)

        t = np.arange(0, self.t_max, dt)
        omega_d = self.omega_n * np.sqrt(1 - self.zeta**2)  # Damped natural frequency
        theta = self.theta0 * np.exp(-self.zeta * self.omega_n * t) * np.cos(omega_d * t)  # Angle in radians
        theta_deg = np.rad2deg(theta)  # Convert angle to degrees

        return t, theta_deg, z

    def plot_oscillations(self):
    
        t, theta, z = self.simulate()

        t_deploy = self.flight_stages.t_deploy
        t_inflation = t_deploy + self.flight_stages.t_inflation

        # Altitude at deployment and end of inflation
        # Assuming terminal velocity is constant during inflation
        v_term = self.terminal_velocity
        z_deploy = self.z0 - v_term * t_deploy
        z_inflation = self.z0 - v_term * t_inflation

        plt.figure(figsize=(10, 5))

        # --- Plot Angle vs Time ---
        plt.subplot(1, 2, 1)
        plt.plot(t, theta, label="Angle of Attack")
        plt.axvline(t_deploy, color='orange', linestyle='--', label="Deployment")
        plt.axvline(t_inflation, color='blue', linestyle='--', label="End of Inflation")
        plt.xlabel("Time [s]")
        plt.ylabel("Angle of Attack [deg]")
        plt.title("Angle of Attack vs Time")
        plt.grid(True)
        plt.legend()

        # --- Plot Angle vs Altitude ---
        plt.subplot(1, 2, 2)
        plt.plot(z, theta, label="Angle of Attack")
        plt.axhline(y=theta[0], color='gray', linestyle=':')  # opcional
        plt.axvline(z_deploy, color='orange', linestyle='--', label="Deployment")
        plt.axvline(z_inflation, color='blue', linestyle='--', label="End of Inflation")
        plt.xlabel("Altitude [m]")
        plt.ylabel("Angle of Attack [deg]")
        plt.title("Angle of Attack vs Altitude")
        plt.grid(True)
        plt.legend()

        plt.tight_layout()
        plt.show()

# Example usage

p1 = Parachute(diameter=10, drag_coefficient=1.5, shape="reefed", mass=80)
estimator = ParachuteOscillationEstimator(
        parachute=p1,
        flight_stages=td,
        damping_ratio=0.18,
        natural_freq=0.7,
        initial_angle=7.0,
        z0=1000,
        t_max=60)

