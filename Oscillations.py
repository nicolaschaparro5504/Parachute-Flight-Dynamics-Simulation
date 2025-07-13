import numpy as np
import matplotlib.pyplot as plt
from parachute import Parachute

class ParachuteOscillationEstimator:
    def __init__(self, parachute: Parachute, mass=80, damping_ratio=0.15, natural_freq=0.8, initial_angle=5.0, z0=1000, t_max=60):
        """
        Estimate angle of attack oscillations during descent using parachute parameters.
        Args:
            parachute (Parachute): Parachute object
            mass (float): Mass of the system (kg)
            damping_ratio (float): Damping ratio (ζ)
            natural_freq (float): Natural frequency (ω_n) [rad/s]
            initial_angle (float): Initial angle of attack [deg]
            z0 (float): Initial altitude [m]
            t_max (float): Maximum simulation time [s]
        """
        self.parachute = parachute
        self.mass = mass
        self.zeta = damping_ratio
        self.omega_n = natural_freq
        self.theta0 = np.deg2rad(initial_angle)
        self.z0 = z0
        self.t_max = t_max

    def descent_velocity(self):
        """
        Estimate steady descent velocity using drag area from parachute.
        v = sqrt((2 * m * g) / (rho * Cd * A))
        """
        g = 9.81
        rho = 1.225  # air density [kg/m^3]
        CdA = self.parachute.area
        v = np.sqrt((2 * self.mass * g) / (rho * CdA))
        return v

    def simulate(self, dt=0.1):
        """
        Simulate oscillations and descent.
        Returns: time array, angle array, altitude array
        """
        t = np.arange(0, self.t_max, dt)
        omega_d = self.omega_n * np.sqrt(1 - self.zeta**2)
        theta = self.theta0 * np.exp(-self.zeta * self.omega_n * t) * np.cos(omega_d * t)
        theta_deg = np.rad2deg(theta)
        v = self.descent_velocity()
        z = self.z0 - v * t
        z[z < 0] = 0
        return t, theta_deg, z

    def plot_oscillations(self):
        t, theta, z = self.simulate()
        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.plot(t, theta)
        plt.xlabel("Time [s]")
        plt.ylabel("Angle of Attack [deg]")
        plt.title("Angle of Attack vs Time")
        plt.grid(True)

        plt.subplot(1, 2, 2)
        plt.plot(z, theta)
        plt.xlabel("Altitude [m]")
        plt.ylabel("Angle of Attack [deg]")
        plt.title("Angle of Attack vs Altitude")
        plt.grid(True)

        plt.tight_layout()
        plt.show()

# Example usage:
if __name__ == "__main__":
    # Use Parachute class from parachute.py
    p1 = Parachute(diameter=10, drag_coefficient=1.5, shape="reefed", mass=80)
    estimator = ParachuteOscillationEstimator(parachute=p1, mass=80, damping_ratio=0.18, natural_freq=0.7, initial_angle=7.0, z0=1000, t_max=60)
